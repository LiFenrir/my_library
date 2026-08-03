---
title: "Scheduled Sampling"
description: "训练序列生成模型时以递减概率用模型自身输出替代真实 token 以缓解 Exposure Bias"
tags: [concept, fundamentals, ml, sequence-modeling]
created: 2026-07-30
---

# Scheduled Sampling

**核心定义**：Scheduled Sampling 是一种训练策略，在训练自回归序列模型时，以随时间递减的概率使用模型自身生成的 token 替代真实历史 token，从而缩小训练与测试分布的差距。

## 机制

在第 $k$ 个训练步，以概率 $\epsilon_k$ 使用模型自身输出：

$$
x_{<t}^{\text{input}} = \begin{cases}
x_{<t}^{\text{true}} & \text{概率 } 1 - \epsilon_k \\
\hat{x}_{<t}^{\text{model}} & \text{概率 } \epsilon_k
\end{cases}
$$

通常 $\epsilon_k$ 从 0 逐渐增加到接近 1。

## 优缺点

- **优点**：缓解 Exposure Bias，让模型适应自身错误。
- **缺点**：训练目标与真实条件分布不一致，可能导致偏差；实现较复杂。

## 与其他概念的关系

- [[01_Fundamentals/ML/Exposure-Bias|Exposure Bias]] — Scheduled Sampling 试图解决的问题
- [[01_Fundamentals/ML/Teacher-Forcing|Teacher Forcing]] — Scheduled Sampling 改进的训练策略

## 来源

- Bengio et al., 2015, "Scheduled Sampling for Sequence Prediction with Recurrent Neural Networks"
