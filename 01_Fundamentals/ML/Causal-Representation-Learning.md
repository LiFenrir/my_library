---
title: Causal Representation Learning
description: 从观测中学习反映因果结构的表示，使世界模型、策略和控制满足时间因果性
tags:
  - causality
  - representation-learning
  - world-model
  - fundamentals
  - ml
created: 2026-07-28
---

# Causal Representation Learning

**Causal Representation Learning** 强调从原始观测中提取能够反映真实因果结构的表示，使得模型在推理、预测和决策时尊重"原因先于结果"的物理因果性。

## Why

传统关联学习容易学到虚假相关或表面统计规律。在物理世界交互中，智能体需要：
- 区分**相关关系**与**因果关系**；
- 保证当前预测只依赖于过去和当前状态，而非未来信息；
- 支持稳定的长程推理与反事实推断（counterfactual reasoning）。

## Core Idea

### 时间因果性（Temporal Causality）

物理世界是因果的：当前状态只由历史状态与动作决定。建模时应避免让未来 token 影响过去预测。

### 因果注意力掩码（Causal Attention Masking）

在序列模型中通过因果掩码强制每个位置只能 attend 到此前位置，从而将模型约束在因果依赖结构内。

### 自回归世界建模

将世界建模形式化为自回归过程：

$$
o_{t+1:t+K} \sim p_\theta(\cdot \mid o_{\leq t}, a_{<t})
$$

在每个时间步基于完整历史生成未来 chunk，同时通过 KV cache 保持长期上下文。

## Key Properties

| 性质 | 含义 | 反例 |
|------|------|------|
| Causal Consistency | 预测仅依赖过去 | Chunk 内双向注意力让未来影响过去 |
| Persistent Memory | 保留完整历史上下文 | 每个 chunk 独立生成导致失忆 |
| Closed-loop Correction | 实时融入新观测 | 开环长序列 rollout 累积漂移 |

## In Robotics

机器人控制中的因果表示学习尤为关键：
- **VLA 的局限**：端到端 reactive mapping 同时学习视觉、动态与控制，表示纠缠导致样本效率低；
- **视频世界模型**：显式建模状态转移，但 chunk-based 扩散常因双向注意力违反因果；
- **因果世界模型**：用自回归结构和 KV cache 统一视觉动态预测与动作推理。

## Related Concepts

- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 具身智能中的因果世界模型实例
- [[04_Embodied-AI/VLA/World-Model-for-Robotics|World Model for Robotics]] — 机器人世界模型综述
- [[01_Fundamentals/ML/Autoregressive-Model|Autoregressive Model]] — 自回归序列建模
- [[03_Robotics/Control/Inverse-Dynamics|Inverse Dynamics]] — 从状态转移反推动作

## Papers

- [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]] — 通过因果注意力与自回归结构实现机器人控制的世界模型
