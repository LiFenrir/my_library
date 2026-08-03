---
title: "Fast-WAM: Do World Action Models Need Test-time Future Imagination?"
description: "证明世界动作模型在测试时无需未来想象即可保持性能，显著提升推理速度。"
tags: ["世界动作模型", "WAM", "视频协同训练", "推理效率", "清华大学", "Galaxea AI"]
created: 2026-07-15
---

# Fast-WAM: Do World Action Models Need Test-time Future Imagination?

## 基本信息

- **作者**: Tianyuan Yuan, Zibin Dong, Yicheng Liu, Hang Zhao
- **机构**: 清华大学 (IIIS), Galaxea AI
- **链接**: https://arxiv.org/abs/2603.16666
- **项目页**: https://yuantianyuan01.github.io/FastWAM/
- **发表**: arXiv 2025

## 研究背景与核心问题

### WAM 的 imagine-then-execute 范式
现有 World Action Models (WAMs) 遵循"先想象后执行"范式：
1. 生成未来观测 $v_{1:T}$
2. 基于想象的未来预测动作 $a_{1:H}$

$$p(a_{1:H} | o, l) = \int p(v_{1:T} | o, l) p(a_{1:H} | o, l, v_{1:T}) dv_{1:T}$$

**问题**: 迭代视频去噪带来巨大测试时延迟。

### 核心问题
WAM 的有效性来自两个因素：
1. **训练时视频预测目标**: 帮助模型学习物理先验和动作条件表示
2. **测试时显式未来生成**: 为动作预测提供额外预见

现有 WAM 将这两个因素纠缠在一起，**难以区分哪个因素真正贡献了性能提升**。

## 核心方法

### Fast-WAM 架构

![[99_Attachments/papers/images/fast-wam/fastwam_fig1_paradigms.jpg]]

**核心思想**: 保留训练时视频协同训练，但跳过测试时未来预测。

**架构设计**:
- **骨干**: Wan2.2-5B 视频 DiT
- **动作专家**: 1B DiT（隐藏维度 1024）
- **总参数量**: 6B
- **架构**: Mixture-of-Transformer (MoT) + 共享注意力

![[99_Attachments/papers/images/fast-wam/fastwam_fig2a_architecture.jpg]]
![[99_Attachments/papers/images/fast-wam/fastwam_fig2b_masks.jpg]]

**训练时**:
- 联合流匹配目标：动作预测 + 视频协同训练
- 结构化注意力掩码：
  - 未来视频 token 在视频分支内双向注意力
  - 动作 token 在动作分支内双向注意力
  - **动作 token 不能关注未来视频 token**（防止未来信息泄露）
  - 干净首帧 token 不关注任何其他 token

**测试时**:
- **完全移除未来视频分支**
- 仅保留干净首帧潜在 token
- 视频骨干单次前向传播 → 产生潜在世界表示
- 动作专家直接生成动作

**训练目标**:
$$\mathcal{L} = \mathcal{L}_{\text{act}} + \lambda \mathcal{L}_{\text{vid}}$$

### 受控变体（用于消融研究）

| 变体 | 描述 | 代表范式 |
|------|------|---------|
| **Fast-WAM** | 本文方法：训练时视频协同训练，测试时直接动作生成 | 无测试时想象 |
| **Fast-WAM-Joint** | 联合去噪：未来视频和动作 token 一起去噪 | DreamZero, UWM |
| **Fast-WAM-IDM** | 视频→动作：先生成未来视频，再条件动作预测 | LingBot-VA, Vidar |
| **Fast-WAM w.o. video co-train** | 移除视频协同训练目标 | 纯 VLA |

## 实验结果

### RoboTwin 2.0 仿真基准

| 方法 | 具身预训练 | Clean | Randomized | Average |
|------|-----------|-------|-----------|---------|
| π₀ | ✓ | 65.92% | 58.40% | 62.2% |
| π₀.₅ | ✓ | 82.74% | 76.76% | 79.8% |
| Motus | ✓ | 88.66% | 87.02% | 87.8% |
| Motus (from WAN2.2) | ✗ | 77.56% | 77.00% | 77.3% |
| LingBot-VA | ✓ | 92.90% | 91.50% | 92.2% |
| LingBot-VA (from WAN2.2) | ✗ | 80.60% | - | 80.6% |
| **Fast-WAM** | **✗** | **91.88%** | **91.78%** | **91.8%** |
| Fast-WAM-Joint | ✗ | 90.84% | 90.32% | 90.6% |
| Fast-WAM-IDM | ✗ | 91.16% | 91.34% | 91.3% |
| Fast-WAM w.o. video co-train | ✗ | 82.76% | 84.80% | 83.8% |

**关键发现**:
- Fast-WAM **无需具身预训练** 即可达到 91.8%，接近 LingBot-VA (92.2%) 和超越 Motus (87.8%)
- Fast-WAM 与 imagine-then-execute 变体（Joint 90.6%, IDM 91.3%）**性能相当**
- **移除视频协同训练导致大幅下降到 83.8%**（-8%）

### LIBERO 仿真基准

| 方法 | 具身预训练 | Spatial | Object | Goal | Long | Average |
|------|-----------|---------|--------|------|------|---------|
| OpenVLA | ✓ | 84.7% | 88.4% | 79.2% | 53.7% | 76.5% |
| π₀ | ✓ | 96.8% | 98.8% | 95.8% | 85.2% | 94.1% |
| π₀.₅ | ✓ | 98.8% | 98.2% | 98.0% | 92.4% | 96.9% |
| LingBot-VA | ✓ | 98.5% | 99.6% | 97.2% | 98.5% | 98.5% |
| Motus | ✓ | 96.8% | 99.8% | 96.6% | 97.6% | 97.7% |
| **Fast-WAM** | **✗** | **98.2%** | **100.0%** | **97.0%** | **95.2%** | **97.6%** |
| Fast-WAM-Joint | ✗ | 99.6% | 99.4% | 98.2% | 96.8% | 98.5% |
| Fast-WAM-IDM | ✗ | 98.8% | 97.8% | 97.8% | 97.6% | 98.0% |
| Fast-WAM w.o. video co-train | ✗ | 89.2% | 99.2% | 95.4% | 90.0% | 93.5% |

**关键发现**:
- Fast-WAM 97.6% 接近 LingBot-VA (98.5%) 和 Motus (97.7%)
- 与 imagine-then-execute 变体性能差距很小（<1%）
- **移除视频协同训练下降到 93.5%**（-4.1%，Spatial 和 Long 下降最明显）

### 真实世界：毛巾折叠任务

![[99_Attachments/papers/images/fast-wam/fastwam_fig3_realworld.jpg]]
![[99_Attachments/papers/images/fast-wam/fastwam_fig4_results_a.jpg]]
![[99_Attachments/papers/images/fast-wam/fastwam_fig4_results_b.jpg]]

在 Galaxea R1 Lite 平台上评估长程毛巾折叠任务（60 小时遥操作数据）：

| 指标 | Fast-WAM | Fast-WAM-Joint | Fast-WAM-IDM | Fast-WAM w.o. video co-train |
|------|----------|----------------|--------------|------------------------------|
| **成功率** | ~60% | ~65% | ~70% | **10%** |
| **完成时间** | 较短 | 中等 | 较长 | **最长** |
| **推理延迟** | **190 ms** | - | **810 ms** | - |

**关键发现**:
- Fast-WAM-IDM 成功率最高但延迟 810ms（4× 慢于 Fast-WAM）
- **移除视频协同训练导致灾难性下降到 10%**
- Fast-WAM 在成功率和速度之间取得最佳平衡

## 核心结论

### 回答核心问题

**"WAM 需要测试时未来想象吗？"**

**答案：不需要。视频协同训练才是主要价值来源。**

证据：
1. Fast-WAM（无测试时想象）与 imagine-then-execute 变体性能相当
2. 移除视频协同训练导致大幅性能下降（-4~8%）
3. 真实世界中移除视频协同训练导致灾难性失败（10% vs 60-70%）

### 视频预测在 WAM 中的真正价值

| 方面 | 测试时未来生成 | 训练时视频协同训练 |
|------|---------------|-------------------|
| **对性能的贡献** | 有限（<1% 差距） | **主导**（-4~8% 下降） |
| **推理成本** | 高（4× 延迟） | 无额外成本 |
| **物理先验学习** | 无直接贡献 | **塑造世界 grounded 表示** |

**核心洞察**: 视频预测的主要价值在于**训练时塑造更好的世界表示**，而非**测试时生成未来观测**。

## 与 WAM 五部曲的关系

| 论文 | 测试时未来生成 | 核心贡献 |
|------|---------------|---------|
| **DreamZero** | ✓ 联合去噪 | 零样本泛化 |
| **LingBot-VA** | ✓ 自回归视频→动作 | 因果一致性、长程记忆 |
| **Cosmos Policy** | ✓ 潜在帧注入（视频+动作+价值） | 极简适配、显式规划 |
| **Motus** | ✓ 三专家 MoT 联合生成 | 统一五范式、光流跨本体 |
| **Fast-WAM** | **✗ 跳过** | **证明测试时生成非必需** |

**Fast-WAM 的意义**:
- 为 WAM 设计提供了新的简化方向
- 证明视频协同训练本身足以获得 WAM 的大部分收益
- 4× 推理加速使 WAM 更适合实时部署

## 局限性与未来工作

1. **规模效应**: 未研究更大规模预训练数据和模型缩放的影响
2. **长程任务**: 当前聚焦单动作块生成，未包含外自回归循环
3. **规划能力**: 未探索基于显式未来生成的规划是否仍有独特价值
4. **泛化测试**: 主要在标准基准上测试，更复杂场景待验证

## 个人评价

**重要性**: ★★★★★
- 提出了 WAM 领域的基础性问题，并通过严谨的受控实验给出了明确答案
- 证明 WAM 可以大幅简化（跳过测试时视频生成），同时保持性能
- 4× 推理加速对实际部署意义重大
- 为 WAM 设计提供了新的理论指导

**对 WAM 方向的启示**:
1. **训练时视频目标 > 测试时视频生成**: 未来 WAM 可以专注于如何更好地利用视频协同训练，而非复杂的测试时生成机制
2. **VLA + 视频协同训练 = WAM**: Fast-WAM 本质上是在 VLA 架构上添加视频协同训练目标
3. **效率与性能可以兼得**: 无需牺牲性能即可获得实时推理

**可改进方向**:
- 探索 Fast-WAM + 显式规划（如 Cosmos Policy 的 Best-of-N）的组合
- 研究更大规模视频预训练对 Fast-WAM 的影响
- 将 Fast-WAM 的自回归扩展与 LingBot-VA 的闭环机制结合

## 相关论文

- [DreamZero](https://arxiv.org/abs/2602.15922) - 联合去噪 WAM
- [LingBot-VA](https://arxiv.org/abs/2601.21998) - 因果自回归 WAM
- [Cosmos Policy](https://arxiv.org/abs/2601.16163) - 视频模型微调策略
- [Motus](https://arxiv.org/abs/2512.13030) - 统一五范式 WAM
- [VPP](https://arxiv.org/abs/2412.14803) - 基于预测视觉表示的策略
- [UVA](https://arxiv.org/abs/2503.00200) - 统一视频动作模型（跳过视频解码）


## 原文

[[05_Papers/articles/fast-wam|fast-wam]]
