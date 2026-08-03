---
title: "World Action Models are Zero-shot Policies"
description: "将世界动作模型作为零样本策略，利用视频生成先验实现高效机器人学习。"
tags: ["世界动作模型", "VLA", "视频扩散", "机器人学习", "跨本体迁移", "零样本泛化", "NVIDIA"]
created: 2026-07-15
---

# World Action Models are Zero-shot Policies

## 基本信息

- **作者**: Seonghyeon Ye†, Yunhao Ge*, Kaiyuan Zheng*, Shenyuan Gao*, Sihyun Yu*, George Kurian*, Suneel Indupuru*, You Liang Tan*, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie, Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen Chebotar, Scott Reed, Jan Kautz, Yuke Zhu†, Linxi "Jim" Fan†, Joel Jang†
- **机构**: NVIDIA
- **链接**: https://arxiv.org/abs/2602.15922
- **项目页**: https://dreamzero0.github.io
- **代码**: https://github.com/dreamzero0/dreamzero
- **发表**: arXiv 2025

## 研究背景与动机

### VLA 的局限性
当前 Vision-Language-Action (VLA) 模型虽然擅长语义泛化（如识别不同物体并执行移动指令），但在以下方面存在明显不足：
- **新动作泛化差**: 无法执行训练数据中未出现的物理动作（如"解开鞋带"）
- **环境泛化有限**: 需要为每个新环境收集大量任务特定数据
- **依赖重复演示**: 传统方法需要每个任务数百次重复演示

根本原因在于：VLM 预训练捕获的是"做什么"的语义知识，但缺乏"如何做"的物理动力学、几何和运动控制表示。

### 核心洞察
视频是世界的密集表示——它编码了物理动力学、空间关系和动作执行方式。通过联合预测视频和动作，模型可以：
1. 从视频预训练继承丰富的时空先验
2. 将动作学习转化为逆动力学问题（从预测的视觉未来提取动作）
3. 利用视频生成作为隐式视觉规划器指导动作生成

## 核心方法

### World Action Model (WAM) 定义
WAM 联合建模视频和动作的联合分布：
$$p(\mathbf{o}_{t:t+H}, \mathbf{a}_{t:t+H} | \mathbf{o}_{0:t}, \mathbf{c})$$

直接产生与预测视觉未来对齐的动作轨迹，无需测试时优化。

### DreamZero 架构

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig4_architecture.jpg]]
![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig4_architecture_b.jpg]]

**输入**: 视觉上下文（VAE 编码）、语言指令（文本编码器）、本体感受状态（状态编码器）
**骨干**: 14B 参数的自回归 DiT（Diffusion Transformer），基于 Wan2.1-I2V-14B-480P 预训练视频扩散模型
**输出**: 未来视频帧 + 对应动作

**关键设计选择**:
1. **端到端联合去噪**: 单一模型同时去噪视频和动作隐变量，共享目标函数确保模态深度整合
2. **自回归架构**: 
   - 利用 KV Cache 实现高效推理
   - 视觉历史作为下一步生成的指导
   - 避免双向模型的模态对齐挑战（视频/动作/语言）
   - 保持原生帧率，确保视频-动作精确对齐
3. **闭环执行**: 每个动作块执行后，用真实观测替换 KV Cache 中的预测帧，消除误差累积

**训练目标** (Flow Matching):
$$\mathcal{L}(\theta) = \mathbb{E}_{\mathbf{z}, \mathbf{a}, \{t_k\}} \left[ \frac{1}{K} \sum_{k=1}^{K} w(t_k) \| \mathbf{u}_\theta([\mathbf{z}_{t_k}^k, \mathbf{a}_{t_k}^k]; \mathcal{C}_k, \mathbf{c}, \mathbf{q}_k, t_k) - \mathbf{v}^k \|^2 \right]$$

采用 Teacher Forcing：模型在干净的历史上下文条件下对当前噪声块进行去噪。

### DreamZero-Flash: 解耦噪声调度

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig5_flash.jpg]]
![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig5_flash_b.jpg]]

**问题**: 标准训练共享视频和动作的噪声时间步，但少步推理需要从高噪声视频中预测干净动作。

**解决方案**: 解耦噪声调度
- 视频时间步偏向高噪声: $t_k^{\text{video}} = 1 - \eta, \quad \eta \sim \text{Beta}(7, 1)$
- 动作时间步保持均匀: $t_k^{\text{action}} \sim \mathcal{U}(0, 1)$

效果: 将扩散步数从 4 步减至 1 步，推理延迟从 ~350ms 降至 ~150ms，性能仅下降 9%。

### 实时推理优化 (38× 加速)

| 优化层级 | 技术 | 加速效果 |
|---------|------|---------|
| **系统级** | CFG 并行（双 GPU） | 1.9× |
| | DiT Cache（速度方向一致性） | 5.5× |
| **实现级** | Torch Compile + CUDA Graphs | 8.9× |
| | Kernel & 调度器优化 | 9.6× |
| | NVFP4 量化 (GB200) | 16.6× |
| **模型级** | DreamZero-Flash | **38×** |

最终达到 **7Hz 实时闭环控制**（从原始 5.7s 降至 150ms）。

## 实验结果

### 数据收集策略

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig6a_duration.jpg]]
![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig6b_subtask.jpg]]
![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig6c_skills.jpg]]

- **500 小时**遥操作数据，覆盖 **22 个真实环境**（家庭、餐厅、超市、咖啡店、办公室等）
- **任务多样性 > 重复性**: 每个环境执行粗粒度任务（如"整理"），平均每段 4.4 分钟包含 ~42 个子任务
- 任务淘汰机制：每个任务收集 50 段后淘汰，强制操作员提出新任务

### Q1: WAM 能否从多样化非重复数据有效学习？

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig8_seen_tasks.jpg]]

**Seen Tasks（新环境、新物体）**:
- DreamZero: **62.2%** 平均任务进度
- 最佳预训练 VLA 基线 (π₀.₅): **27.4%**
- **>2× 提升**，尽管基线已在数千小时跨本体数据上预训练

**关键发现**: 从头训练的 VLA 几乎为零（<1%），表明 VLA 难以从异构数据学习；WAM 的视频生成先验使多样化数据学习成为可能。

### Q2: WAM 能否泛化到未见过任务？

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig9_unseen_tasks.jpg]]

**Unseen Tasks（训练分布外）**:
- DreamZero: **39.5%** 平均任务进度
- 预训练 VLA 基线: **16.3%**
- 从头 VLA: **<1%**

成功案例：解鞋带（85.7%）、握手（59.2%）、熨烫、绘画、堆叠立方体等完全未在训练中出现的行为。

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig2_joint_prediction.jpg]]
![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig2_joint_prediction_b.jpg]]

**视频-动作对齐**: 预测动作与生成视频紧密对齐，即使对未见任务也是如此。

### Q3: WAM 微调后是否保持泛化？

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig10_posttraining.jpg]]

- 在衬衫折叠、水果包装、餐桌清理三个任务上微调后：
- DreamZero 匹配或超越 VLA 基线
- **环境泛化能力在微调后仍然保持**（在未见环境中评估）

### Q4: WAM 能否实现跨本体迁移？

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig11_cross_embodiment.jpg]]

**仅使用视频数据（无动作标签）**：
- Robot-to-Robot (YAM → AgiBot): 38.3% → **55.4%** (+45%)
- Human-to-Robot (人类 → AgiBot): 38.3% → **54.3%** (+42%)
- 仅需 **10-20 分钟** 视频数据

**意义**: 不同于 VLA 需要动作标注的迁移方法，WAM 仅需视觉信息即可实现有意义的迁移。

### Q5: WAM 能否实现少样本新本体适应？

![[99_Attachments/papers/images/world-action-models-zero-shot/wam_fig12_few_shot.jpg]]

- 用仅 **30 分钟**（55 段，11 个任务）的 YAM 机器人游戏数据微调
- 保留强大的语言跟随能力
- 泛化到未见物体（南瓜、泰迪熊、笔、杯面、纸袋）
- 观察到紧密的视频-动作对齐

### Q6: DreamZero-Flash 能否保持性能？

| 方法 | 去噪步数 | 任务进度 | 推理速度 |
|------|---------|---------|---------|
| DreamZero | 4 | 83% | 350ms |
| DreamZero | 1 | 52% | 150ms |
| **DreamZero-Flash** | **1** | **74%** | **150ms** |

Flash 在单步推理下恢复 4 步性能的 89%，速度提升 2.33×。

### 消融实验

**数据多样性**:
- 重复数据: 33% ± 4.2%
- 多样化数据: **50% ± 6.3%** (+52%)

**模型规模**:
- 5B: 21% ± 4.2%
- **14B**: **50% ± 6.3%** (+138%)
- VLA 5B/14B 在多样化数据上: **0%**（完全失败）

**架构（自回归 vs 双向）**:
- 任务进度相似（50%），但 AR 产生更平滑的动作，推理快 3-4×

## 关键结论

1. **WAM 从根本上优于 VLA 的数据效率**: 视频生成先验使从异构非重复数据有效学习成为可能
2. **模型规模直接转化为策略性能**: 与 VLA 不同，WAM 表现出清晰的规模扩展行为
3. **自回归架构更适合闭环控制**: KV Cache 高效、保持原生帧率、动作更平滑
4. **跨本体迁移仅需视频**: 无需动作标注，10-20 分钟视频即可显著提升未见任务性能
5. **少样本适应可行**: 30 分钟新本体数据即可实现零样本泛化
6. **推理速度可达实时**: 38× 加速实现 7Hz 闭环控制

## 局限性与未来工作

1. **长程推理**: 当前为 System 1 模型（6 秒上下文），需 System 2 规划器或扩展上下文窗口
2. **高精度任务**: 亚厘米级精度任务（如钥匙插入）仍是挑战
3. **计算成本**: 相比 VLA（20Hz+ 消费级 GPU），DreamZero 仍需 2×GB200
4. **规模定律**: 模型大小、数据量、计算量的最优配置待探索
5. **野外人类数据**: 仅使用 12 分钟实验室人类数据，大规模野外视频数据潜力待挖掘

## 与其他世界模型架构对比

| 架构 | 表示空间 | 测试时优化 | 实时控制 |
|------|---------|-----------|---------|
| **WAM (DreamZero)** | 像素空间 | 无需 | **7Hz** |
| JEPA/V-JEPA | 隐空间 | 需要规划/搜索 | 挑战 |
| Dreamer | 隐空间 | 需要 MPC | 挑战 |
| PointWorld | 3D 点云 | 需要 MPPI 采样 | 挑战 |

WAM 的核心优势：联合建模视频和动作，直接产生动作轨迹，无需测试时优化。

## 个人评价

**重要性**: ★★★★★
- 首次系统性地展示了 World Action Model 在真实机器人上的全面优势
- 提出了"视频生成质量 = 策略性能"的深刻洞察
- 开源 14B 模型权重和推理代码，推动社区发展

**创新点**:
1. 将视频扩散模型成功转化为实时机器人策略
2. 解耦噪声调度（Flash）实现速度-精度平衡
3. 数据多样性优先于重复性的反直觉策略得到验证
4. 跨本体迁移仅需视频，大幅降低数据收集成本

**可改进方向**:
- 探索更小的视频骨干模型以实现边缘设备部署
- 结合 System 2 规划器处理长程任务
- 利用大规模野外人类视频数据（如 Ego4D）进一步扩展

## 相关论文

- [π₀](https://arxiv.org/abs/2410.24164) - VLA flow model baseline
- [GR00T N1](https://arxiv.org/abs/2503.14734) - NVIDIA humanoid VLA
- [OpenVLA](https://arxiv.org/abs/2406.09246) - Open-source VLA
- [Cosmos Policy](https://arxiv.org/abs/2601.16163) - Concurrent WAM work
- [DROID](https://arxiv.org/abs/2403.12945) - 多样化机器人操作数据集


## 原文

[[05_Papers/articles/world-action-models-zero-shot|world-action-models-zero-shot]]
