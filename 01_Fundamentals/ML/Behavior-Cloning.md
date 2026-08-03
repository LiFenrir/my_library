---
title: Behavior Cloning
description: 通过最大化专家动作似然从演示数据中学习策略的模仿学习方法
tags:
  - ml
  - imitation-learning
  - behavior-cloning
  - fundamentals
  - robotics
created: 2026-07-30
---

# Behavior Cloning (BC)

从状态-动作对数据集 $\mathcal{D} = \{ (s_i, a_i) \}$ 中学习策略 $\pi_\theta(a|s)$，通过最大化专家动作似然来复现专家行为。

## Objective

$$
\mathcal{L}_{BC}(\theta) = -\mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ \log \pi_\theta(a|s) \right]
$$

## Limitations

- **数据饥渴**：需要大量高质量演示；
- **复合误差**：测试时一旦偏离训练分布，错误会逐步累积；
- **次优与噪声**：真实演示常含错误、迟疑、重复尝试，标准 BC 无法区分优劣样本；
- **奖励不可知**：不利用任何关于动作好坏的额外信号。

## Extensions

- [[Advantage-Weighted-Behavior-Cloning]]：用学习得到的相对优势对样本加权；
- [[Reward-Aligned-Behavior-Cloning]]：用阶段感知奖励模型对样本加权；
- [[Human-Gated-DAgger]]：在线收集分布内数据以缓解复合误差。

## Related Concepts

- [[Imitation-Learning]] — 更广泛的研究领域
- [[Offline-Reinforcement-Learning]] — 从次优数据中提取更优策略
- [[Advantage-Reward-Modeling]] — 为加权 BC 提供优势信号

## Papers

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]，第 1、3.4 节
- Osa et al., "An Algorithmic Perspective on Imitation Learning", 2018
