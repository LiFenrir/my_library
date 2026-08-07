---
title: "Dual-State TTT Memory"
description: "DexWorldModel 中结合短时前向状态与长时 Test-Time Training 记忆的双状态记忆机制"
tags: [concept, embodied-ai, world-model, memory, test-time-training]
created: 2026-07-30
---

# Dual-State TTT Memory

**核心定义**：Dual-State TTT Memory 是 DexWorldModel 提出的一种双状态记忆机制，将标准前向传播的**短时状态**与通过 Test-Time Training 在线更新的**长时记忆状态**结合，实现常数空间复杂度的长程依赖建模。

## 两个状态

### 1. 短时状态 $h_t$

- 由当前观测和前一步短时状态经标准前向传播得到；
- 负责当前步的即时预测；
- 与标准 Transformer 的隐状态类似。

### 2. 长时记忆状态 $m_t$

- 通过 Test-Time Training 在 episode 运行过程中持续更新；
- 编码 episode 级别的上下文和动态适应信息；
- 大小固定，不随序列长度增长。

## 更新机制

在每个时间步，利用当前真实观测与模型预测之间的差异更新长时记忆：

$$
m_{t+1} = \text{TTT-Update}(m_t, o_t, \hat{o}_t; \theta_{\text{mem}})
$$

其中 $\theta_{\text{mem}}$ 是少量的记忆专用参数。

## 优势

- **常数空间复杂度**：无论 episode 多长，记忆大小固定；
- **在线适应**：测试时根据当前环境动态调整；
- **避免 KV cache 线性增长**：适合长程机器人任务和边缘部署。

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/test-time-training-for-world-models|Test-Time Training for World Model[[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — Dual-State TTT Memory 所属的技术框架
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]]|Causal Latent World Mode[[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 使用该记忆机制的世界模型
- [[01_Fundamentals/ML/Catastrophic-Forgetting|Catastrophic Forgettin[[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — TTT 更新需避免覆盖关键记忆

## 来源

- [[05_Papers/articles/dexworldmodel|DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Task[[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]]
