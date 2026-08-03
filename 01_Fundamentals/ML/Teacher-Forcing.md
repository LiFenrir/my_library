---
title: Teacher Forcing
description: 训练序列生成模型时使用真实历史 token 作为上下文而非模型自身生成的输出
tags:
  - fundamentals
  - ml
  - sequence-modeling
  - autoregressive
  - training-technique
created: 2026-07-30
---

# Teacher Forcing

**Teacher Forcing** 是训练自回归序列模型的一种策略：在预测第 $t$ 个 token 时，使用数据中的真实历史 token $x_{<t}$ 作为上下文，而不是模型自己生成的历史输出。

## Core Idea

自回归模型理论上应基于自身之前生成的输出继续生成：

$$
x_t \sim p_\theta(\cdot \mid x_1, \dots, x_{t-1})
$$

Teacher Forcing 在训练时改用 ground-truth 序列：

$$
\mathcal{L} = -\sum_t \log p_\theta(x_t \mid x_{<t}^{\text{true}})
$$

这样可以避免训练早期模型输出质量差导致的错误累积，降低优化难度。

## Exposure Bias

Teacher Forcing 的潜在问题是训练与测试分布不一致：测试时模型必须依赖自己生成的历史。这种差异称为 **Exposure Bias**。缓解方法包括：

- **Scheduled Sampling**：以一定概率使用模型自身输出代替真实 token；
- **Data Noising**：向输入加入噪声提高鲁棒性；
- **RL/SeqGAN 训练**：直接优化测试时生成质量。

## In Robotics World Models

在机器人世界模型中，Teacher Forcing 具有特殊优势：

- 部署时机器人会不断从真实环境获得新观测，这些观测与训练数据分布一致；
- 因此模型在测试时仍然条件于 "真实" 历史（来自环境反馈），与 Teacher Forcing 训练机制自然匹配；
- 相较于纯生成任务，Exposure Bias 问题被显著削弱。

## 优缺点

- **优点**：
  - 训练稳定、收敛快；
  - 可并行计算所有时间步的损失；
  - 对机器人控制场景与真实反馈天然兼容。
- **缺点/局限**：
  - 纯生成任务中存在 Exposure Bias；
  - 过度依赖真实历史可能降低对模型自身错误的鲁棒性。

## Related Concepts

- [[01_Fundamentals/ML/Autoregressive-Model|Autoregressive Model]] — Teacher Forcing 的训练对象
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 使用 Teacher Forcing 统一训练视频-动作序列
- [[01_Fundamentals/ML/Exposure-Bias|Exposure Bias]] — Teacher Forcing 的经典问题
- [[01_Fundamentals/ML/Scheduled-Sampling|Scheduled Sampling]] — 缓解 Exposure Bias 的方法

## Papers

- [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]] — 第 3.3 节讨论 Teacher Forcing 在机器人世界模型中的适用性
