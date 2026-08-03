---
title: innov_openpi 训练损失尖峰复盘
description: 右臂夹爪低方差导致 quantile 归一化放大，引发 flow matching loss 尖峰
tags: [experiment, innov_openpi, vla, normalization, data-quality, flow-matching]
created: 2026-07-23
---

# innov_openpi 训练损失尖峰复盘

## 实验背景

- **时间**：2026-07-23
- **项目**：[[06_Projects/own/innov-openpi|innov_openpi]]
- **任务**：基于 OpenPI 框架对 π₀.₅ 做 SFT 微调
- **模型**：π₀.₅ = PaliGemma 2B + Gemma 300M，flow matching 动作生成
- **训练脚本**：`scripts/train_pytorch.py`
- **关键配置**：`batch_size=32`, `clip_gradient_norm=1.0`, `use_quantile_norm=True`（pi05 默认启用）

## 出现的问题

使用 `configs/innov_arm/0720_paper_cup.yaml` 训练时，loss 曲线出现**周期性尖峰**，类似如下特征：

- 大部分 step 的 loss 正常
- 每隔一段时间出现一次比正常值大 3~4 个数量级的尖峰
- 尖峰后 loss 能回落，但反复出现
- 同一模型、同一网络、同一超参下，换用 `configs/innov_arm/pi05_finetune_innov_arm.yaml` 后训练平稳，无尖峰

## 对比两个配置

| 配置 | 数据集 | asset_id | 右臂夹爪（dim13）统计 |
|------|--------|----------|----------------------|
| `0720_paper_cup.yaml` | `/home/kemove/INNOV/datasets/innov_arm/innov_0722_backup` | `innov_arm_0722_backup` | mean≈1.0，std≈0.0047，q01≈q99≈1.0 |
| `pi05_finetune_innov_arm.yaml` | `/home/kemove/INNOV/datasets/innov_arm/innov_0722` | `innov_arm_0722` | 全为 0 |

**两个数据集唯一区别**：后者把右臂关节（包括夹爪）全部硬置为 0。

## 问题原因

### 1. 数据分布：右臂夹爪几乎恒为闭合

在 `innov_0722_backup` 中，右臂夹爪（dim13）绝大多数帧都是闭合状态（≈1.0），只有极少数帧打开到 0.0 附近。这导致 `compute_norm_stats.py` 计算出的分位数统计量为：

- `q01 ≈ 0.99966`
- `q99 ≈ 1.00004`
- `q99 - q01 ≈ 3.8e-4`

### 2. π₀.₅ 默认启用 quantile 归一化

`src/openpi/training/config.py:174`：

```python
use_quantile_norm=model_config.model_type != ModelType.PI0
```

pi05 会走 quantile 归一化，对应实现：

`src/openpi/transforms.py:141-145`：

```python
def _normalize_quantile(self, x, stats: NormStats):
    assert stats.q01 is not None
    assert stats.q99 is not None
    q01, q99 = stats.q01[..., : x.shape[-1]], stats.q99[..., : x.shape[-1]]
    return (x - q01) / (q99 - q01 + 1e-6) * 2.0 - 1.0
```

当夹爪打开到 0.0 时，归一化后：

```
(0.0 - 0.99966) / (3.8e-4 + 1e-6) * 2 - 1 ≈ -5200
```

这一维度的动作目标从正常 `[-1, 1]` 跳到 **-5200 左右**。

### 3. 直接进入 flow matching loss

`src/openpi/models_pytorch/pi0_pytorch.py:340-386`：

```python
x_t = time_expanded * noise + (1 - time_expanded) * actions
u_t = noise - actions
...
return F.mse_loss(u_t, v_t, reduction="none")
```

`actions` 已经经过归一化，`u_t` 在 dim13 上也是 `-5e3` 量级。MSE 平方后，单帧 loss 达到 **10^7 量级**，即使 `clip_gradient_norm=1.0` 也只能压梯度，loss 本身仍会呈现尖峰。

### 4. 梯度裁剪反而放大异常样本权重

`clip_gradient_norm=1.0` 会把整个 batch 的梯度缩放到范数 1。异常样本产生的梯度范数可能已经是 1000+，裁剪后整个 batch 的更新方向几乎完全由这 1 个样本决定；正常样本的梯度被同比例压缩到接近 0。

**结果**：有效 batch 被异常样本"劫持"，模型不是在学大多数正常数据，而是在拟合极少数离群点。

### 5. 右臂其他低方差维度也是隐患

backup 统计中，右臂 dim8（std≈8e-4）、dim11（std≈1e-3）等也非常小。这些维度只要有轻微运动，归一化后也会放大几十到几百倍，同样贡献 loss 噪声。dim13 只是因为"闭合≈1.0 / 打开≈0.0"的极端分布，表现得最尖锐。

### 6. 为什么 `innov_0722` 没问题

`innov_0722` 把右臂所有维度恒置为 0，统计值：

```
q01 = q99 = 0
std = 0
```

归一化后：

```
(0 - 0) / (0 + 1e-6) * 2 - 1 = 0
```

动作目标和状态都恒为 0，不会触发异常。代价是右臂完全不动。

## 如何解决

### 方案 A：数据侧修正（推荐）

把右臂夹爪的"恒闭合"问题在数据层面解决，而不是靠归一化层硬扛：

1. **检查示教数据**：确认右臂是否真的应该参与任务；如果不参与，应在训练前就把右臂相关维度统一置 0（如 `innov_0722` 的做法）。
2. **不要混合"几乎恒值 + 少量真实变化"的维度**：这种维度会让 quantile 归一化产生灾难性放大。
3. **数据预处理时剔除或合并低方差维度**：如果某关节 std < 1e-3，考虑在数据集中固定为常数。

### 方案 B：归一化侧保护

如果数据无法修改，可在归一化层增加保护：

1. **对极低方差维度设置最小 range**：例如 `(q99 - q01 + 1e-6)` 中的 epsilon 可改为按维度自适应的最小阈值。
2. **clip 归一化输出**：把归一化后动作限制在 `[-10, 10]` 或 `[-3, 3]`，防止极端值进入网络。
3. **改用 z-score 归一化**：对 pi05 也可选择不使用 quantile，改用 z-score，但对长尾分布不友好。

### 方案 C：训练侧缓解

1. **过滤异常样本**：在 data loader 中检测归一化后 action 的 max abs，超过阈值则跳过或 clip。
2. **增大 gradient clip**：从 1.0 提高到 10.0 或 100.0，让正常样本梯度不被过度压缩（但不能解决根本问题）。
3. **loss 加权或 robust loss**：用 Huber loss 替代 MSE，降低离群点影响。

### 本次实际采用的方案

最终采用与 `innov_0722` 一致的做法：在训练数据预处理阶段把右臂关节（含夹爪）统一置 0，避免低方差维度进入训练。

## 部署影响

如果直接部署使用 `innov_0722_backup` 训练出的模型，会出现以下问题：

### 1. 状态离散化输入失真

π₀.₅ 把 state 作为离散语言 token 输入：`src/openpi/models/tokenizer.py:26`

```python
discretized_state = np.digitize(state, bins=np.linspace(-1, 1, 256 + 1)[:-1]) - 1
```

当夹爪打开（state=0）时，归一化后变成 -5200，远小于 -1，`np.digitize` 会把它 clip 到最左端 bin；而闭合状态（state=1）归一化后 ≈1.0，对应 bin 255。

**结果**：打开和闭合两种完全不同的物理状态，被编码成几乎相同的 token，视觉-语言模型接收到的状态信息严重失真。

### 2. 训练目标与部署采样空间不匹配

flow matching 采样时，初始 noise 是标准正态 `N(0,1)`，采样轨迹从 `x_1 ∈ [-3,3]` 逐步 denoise 到 `x_0`。训练时虽然见过 `x_t ≈ -5200` 的极端区域，但部署采样几乎不会进入该区域。所以模型输出仍会被限制在 `[-3,3]` 归一化空间，再经反归一化压回 `[0.999,1.000]`。

**简言之**：训练时被强迫学习一个极宽范围，但部署时这个范围用不上，反而把正常输出区间压缩成了一条"夹爪闭合"的直线。

### 3. 对左臂的间接影响

右臂异常不会直接改变左臂统计，但会通过共享 transformer 权重和注意力机制影响整体策略。模型为了拟合右臂异常 target，可能调整 action expert 的共享表示，导致左臂动作精度下降或抖动。

## 后续排查框架

当确认训练参数和网络没问题后，按以下顺序排查数据侧问题：

### 第一层：确认 loss 尖峰形态

| 检查项                 | 方法                                         |
| ------------------- | ------------------------------------------ |
| 尖峰是持续还是偶发           | 看 wandb / tensorboard loss 曲线              |
| 是否伴随梯度范数尖峰          | 记录 `gard per step`                         |
| 是否伴随某维度输出异常         | 打印 `actions` / `v_t` / `u_t` 的 per-dim 最大值 |
| 是否伴随 weight norm 增长 | 监控模型参数 L2 norm                             |

**关键指标**：loss 尖峰但参数 norm 稳定 → 通常是输入 target 异常；参数 norm 同步增长 → 更可能是网络稳定性问题。

### 第二层：定位异常维度

`PI0Pytorch.forward` 返回的 loss 是 `[B, T, D]`：

```python
per_element_loss = self.pi0.forward(observation, actions)
loss_per_dim = per_element_loss.sum(dim=[0,1])
```

找出贡献最大的维度，回查该维度的 `actions` 原始值和归一化值。

### 第三层：检查归一化输出

在训练循环里临时打印：

```python
print("action raw stats:", actions.min(), actions.max(), actions.std())
print("action per-dim max abs:", actions.abs().max(dim=[0,1]).values)
```

如果某维度归一化值远超 `[-3, 3]`，就是归一化层把数据放大了。

### 第四层：回查 norm_stats

```python
from openpi.shared import normalize
stats = normalize.load("assets/<asset_id>")
for key, s in stats["norm_stats"].items():
    print(f"{key} std:", s.std)
    print(f"{key} range:", s.q99 - s.q01 if s.q99 is not None else None)
```

**危险信号**：
- `std < 1e-4`
- `q99 - q01 < 1e-3`
- `q01` 和 `q99` 接近浮点精度边界
- `std == 0.0`

### 第五层：检查原始数据分布

```python
for dim in range(action_dim):
    vals = actions[:, :, dim].flatten()
    print(f"dim{dim}: min={vals.min():.4f}, max={vals.max():.4f}, "
          f"mean={vals.mean():.4f}, std={vals.std():.4f}, "
          f"q01={np.quantile(vals,0.01):.4f}, q99={np.quantile(vals,0.99):.4f}")
```

重点看：是否有恒为常数的维度、是否有极端离群点、不同 episode 间是否有量级差异。

### 数据侧专项排查清单

| 现象 | 数据原因 | 排查 |
|------|---------|------|
| 某维度 std≈0 | 关节恒为固定值 | 检查传感器/硬编码 |
| q01≈q99 但存在少量远离值 | 长尾离群点 | 画直方图 |
| mean 和 median 差异大 | 分布偏斜 | 箱线图 |
| 左右臂统计严重不对称 | 双臂运动幅度不一致 | 分别统计左右半段 |
| 动作跳变 | 插帧/丢帧/示教抖动 | 画时序曲线 |
| prompt 与动作不一致 | 跨模态标注错误 | 可视化检查 |

## 常态化监控建议

### 训练前

运行 `compute_norm_stats.py` 后自动检查：

```python
def validate_norm_stats(stats, action_dim):
    issues = []
    for key in ["state", "actions"]:
        s = stats["norm_stats"][key]
        for d in range(action_dim):
            std = s.std[d]
            qrange = s.q99[d] - s.q01[d] if s.q99 is not None else std
            if std < 1e-4 or qrange < 1e-4:
                issues.append(f"{key}[{d}] low variance: std={std}, qrange={qrange}")
            if std == 0.0:
                issues.append(f"{key}[{d}] zero variance")
    return issues
```

### 训练中

每 N 步记录：

```python
max_abs_action = actions.abs().max().item()
max_abs_state = observation.state.abs().max().item()
max_abs_u = u_t.abs().max().item()
total_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float('inf')).item()
```

阈值告警：
- `max_abs_action > 100` → 归一化异常
- `max_loss_per_dim > 正常均值 * 100` → 存在离群样本
- `total_norm > 1000` → 梯度爆炸

### 部署前

抽查反归一化输出，确认各维度在真实物理范围内。

## 关键结论

1. **损失尖峰不是模型或 RTC 造成的**，而是数据分布 → 统计量 → quantile 归一化 → flow matching loss 的链路被低方差维度放大。
2. **梯度裁剪不能解决根因**，反而会让异常样本主导 batch 更新。
3. **部署比训练更危险**：训练只是 loss 不好看，部署会让夹爪功能直接失效、state 编码失真。
4. **最佳实践**：在数据预处理阶段处理掉"几乎恒值 + 少量真实变化"的维度，而不是让归一化层硬扛。

## 相关

- [[06_Projects/own/innov-openpi|innov_openpi]]
- [[04_Embodied-AI/VLA/index|VLA]]
- #data-quality #normalization #flow-matching #robot-data
