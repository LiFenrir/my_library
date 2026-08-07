---
title: Inverse Dynamics
description: 从期望的状态转移反推产生该转移所需的动作或力
tags:
  - robotics
  - control
  - dynamics
  - manipulation
created: 2026-07-28
---

# Inverse Dynamics

**Inverse Dynamics（逆动力学）** 指从给定的状态转移（如当前状态到目标状态）反推能够产生该转移的动作或控制力。

## Core Idea

与**正向动力学（Forward Dynamics）** 相反：
- 正向动力学：给定动作，预测下一状态；
- 逆动力学：给定当前状态与下一状态，推断所需动作。

## In Robot Learning

在视觉-动作学习中，逆动力学常被用来解耦"世界理解"与"动作生成"：

1. **视觉动态预测**：先预测未来观测；
2. **动作解码**：再基于当前观测与预测观测推断动作：

$$
a_{t:t+K-1} \sim g_\psi(\cdot \mid \hat{z}_{t+1:t+K}, z_{\leq t}, a_{<t})
$$

其中 $z$ 为视觉 VAE 隐状态，$a$ 为动作历史。

## Why It Helps

- **解耦表示学习**：世界模型先学习通用物理动态，可大规模视频预训练；
- **降低动作数据需求**：动作解码器只需机器人示教数据即可将视觉预测映射为可执行动作；
- **提升可解释性**：动作直接对应"实现某视觉变化"的意图。

## Related Concepts

- [[03_Robotics/Control/Forward-Dynamics|Forward Dynamics]] — 给定动作预测下一状态
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 使用逆动力学解码动作的世界模型
- [[03_Robotics/Fundamentals/Dynamics-Model|Dynamics Model]] — 环境动态建模
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — 直接端到端映射的视觉-语言-动作策略

## Papers

- [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]] — 基于预测视觉状态用逆动力学模型解码机器人动作
