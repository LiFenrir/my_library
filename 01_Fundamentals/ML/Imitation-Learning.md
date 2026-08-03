---
title: Imitation Learning
description: 从专家演示中学习策略的机器学习方法，典型代表为行为克隆
tags:
  - ml
  - imitation-learning
  - behavior-cloning
  - fundamentals
  - robotics
created: 2026-07-28
---

# Imitation Learning

从专家演示数据中学习策略，使模型能够复现专家行为。

## Core Idea

给定状态-动作对数据集 $\mathcal{D} = \{ (s_i, a_i) \}$，直接学习策略 $\pi_\theta(a|s)$ 以逼近专家策略。最常用形式是 **Behavior Cloning（BC）**，即最大化专家动作似然：

$$
\mathcal{L}_{BC}(\theta) = -\mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ \log \pi_\theta(a|s) \right]
$$

## Limitations

- **数据饥渴**：需要大量高质量演示；
- **复合误差**：测试时偏离分布会累积；
- **次优与噪声**：复杂长程任务中人类演示常包含错误、迟疑、重复尝试，标准 BC 无法区分优劣样本。

## Extensions

- **DAgger**：在线收集更多分布内数据；
- **Reward-Aligned / Advantage-Weighted BC**：用奖励或优势对样本加权，抑制次优数据；
- **Inverse RL / RLHF**：从偏好或反馈中推断奖励函数。

## Relation to Robotics

VLA 等机器人策略通常以 BC 为基础，再用 [[Offline-Reinforcement-Learning|离线 RL]] 或 [[Advantage-Weighted-Behavior-Cloning|AW-BC]] 等方法进行 refinement。

## Related Concepts

- [[Behavior-Cloning]] — BC 的具体实现与问题
- [[Advantage-Weighted-Behavior-Cloning]] — 优势加权的行为克隆
- [[Offline-Reinforcement-Learning]] — 从离线数据中提取更优策略
- [[Advantage-Reward-Modeling]] — 为加权提供优势信号
- [[Vision-Language-Action]] — 机器人策略模型背景

## Papers

- Osa et al., "An Algorithmic Perspective on Imitation Learning", 2018
- [[arm]] — ARM: Advantage Reward Modeling for Long-Horizon Manipulation
