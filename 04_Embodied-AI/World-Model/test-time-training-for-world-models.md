---
title: "Test-Time Training for World Models"
description: "在测试阶段通过自监督在线更新让世界模型适应当前Episode，实现常数空间复杂度的长程记忆"
tags: [concept, embodied-ai, world-model, test-time-training, memory]
created: 2026-07-30
---

# Test-Time Training for World Models

**核心定义**：Test-Time Training（TTT）for World Models 指在模型部署后的每个 episode 中，利用当前观测序列通过自监督目标在线更新少量网络参数或记忆状态，使世界模型无需依赖 KV cache 即可保持长程一致性和适应性。

## 为什么需要

标准自回归世界模型在长序列推理时面临两难：

- **KV cache**：保存完整历史，显存随序列长度线性增长；
- **固定上下文长度**：截断历史导致遗忘早期关键信息。

TTT 通过在测试时在线学习一个紧凑的「记忆状态」，将长程信息压缩到固定大小的参数或隐变量中。

## 核心机制

### 1. 双状态记忆（Dual-State Memory）

DexWorldModel 采用两个互补状态：

- **短时状态 $h_t$**：标准前向传播产生的隐状态，用于当前步预测；
- **长时状态 $m_t$**：通过 TTT 在每一步更新的慢变记忆状态，编码 episode 级别的上下文。

### 2. 自监督更新目标

在每个时间步，用模型自身的预测与当前真实观测之间的重构误差更新记忆：

$$
m_{t+1} = \text{TTT}(m_t, o_t, \hat{o}_t)
$$

其中更新只作用于少量记忆参数或适配器，保持主体模型冻结。

### 3. 常数空间复杂度

无论 episode 多长，记忆状态大小固定，避免 KV cache 的线性增长。

## 优缺点

- **优点**：
  - 支持任意长 episode；
  - 测试时适应新环境动态；
  - 降低边缘部署显存压力。
- **缺点/局限**：
  - 增加每步推理计算量；
  - 需要设计稳定的自监督更新目标；
  - 分布外场景可能更新失效。

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/causal-latent-world-model|Causal Latent World Model]] — DexWorldModel 的具体实现
- [[04_Embodied-AI/World-Model/World-Model|World Model]] — 应用场景
- [[01_Fundamentals/ML/Catastrophic-Forgetting|Catastrophic Forgetting]] — TTT 需在单 episode 内避免覆盖重要记忆

## 来源

- [[05_Papers/articles/dexworldmodel|DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks]]
