---
title: Regularized Reinforcement Learning
description: 在最大化累积奖励的同时约束策略与参考策略距离的强化学习范式
tags:
  - reinforcement-learning
  - offline-rl
  - regularization
  - concept
created: 2026-07-28
---

# Regularized Reinforcement Learning

在标准 RL 目标上增加对参考策略 $\pi_{\mathrm{ref}}$ 的散度约束，使学习策略既提升回报，又不偏离参考策略太远。

## Core Objective

$$
\mathcal{J}(\pi, \pi_{\mathrm{ref}}) = \mathbb{E}_{\tau \sim \rho_\pi}\left[\sum_{t=0}^{T} \gamma^t r_t\right] - \beta \, \mathbb{E}_{\mathbf{o} \sim \rho_\pi}\left[D\big(\pi(\cdot|\mathbf{o}) \,\|\, \pi_{\mathrm{ref}}(\cdot|\mathbf{o})\big)\right]
$$

- $D$ 为散度度量，常用 KL 散度。
- $\beta$ 控制探索/优化与正则化之间的权衡。

## Why It Matters

- **离线 RL**：参考策略通常是采集数据的 behavior policy，正则化抑制分布偏移。
- ** imitation + RL 混合**：在演示数据上微调时，防止策略偏离专家行为。
- **大模型稳定性**：避免大容量策略（如 VLA）在 RL 更新中崩溃。

## Closed-Form Solution (KL Case)

当 $D$ 为 KL 散度时，最优策略满足：

$$
\hat{\pi}(\mathbf{a}|\mathbf{o}) \propto \pi_{\mathrm{ref}}(\mathbf{a}|\mathbf{o}) \exp\left(\frac{A^{\pi_{\mathrm{ref}}}(\mathbf{o}, \mathbf{a})}{\beta}\right)
$$

这是 [[Advantage-Conditioning]]、AWR、CRR 等离线 RL 方法的共同理论基础。

## Related Concepts

- [[Advantage-Estimation]] — 优势函数是正则化策略改进的核心输入
- [[Policy-Extraction]] — 从值函数或优势中提取改进策略
- [[Offline-Reinforcement-Learning]] — 正则化是离线 RL 的关键稳定器
- [[RECAP]] — 将正则化 RL 思想用于 VLA 的迭代离线训练
