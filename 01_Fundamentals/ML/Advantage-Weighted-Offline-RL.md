---
title: Advantage-Weighted Offline RL
description: 通过优势加权从固定离线数据中提取改进策略的离线强化学习方法族
tags:
  - ml
  - reinforcement-learning
  - offline-rl
  - advantage
  - fundamentals
created: 2026-07-30
---

# Advantage-Weighted Offline RL

从固定离线数据集 $\mathcal{D}$ 中学习策略，通过对样本施加优势相关权重来抑制次优轨迹、优先高价值样本的强化学习方法族。

## Core Idea

在行为克隆目标上引入优势权重，使训练更关注数据分布中“比平均更好”的动作：

$$
\max_\theta \mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ w(s,a) \log \pi_\theta(a|s) \right]
$$

其中 $w(s,a)$ 通常由动作优势 $A(s,a)$ 或值函数导出。

## Representative Methods

- **AWR (Advantage-Weighted Regression)**：用指数化优势作为权重，在监督学习框架下提取策略；
- **AWAC (Advantage-Weighted Actor-Critic)**：结合 Actor-Critic 与优势加权，加速在线学习；
- **IQL (Implicit Q-Learning)**：隐式 Q 学习，避免显式查询学习策略的动作值。

这些方法都属于 [[Offline-Reinforcement-Learning]]，共同假设环境奖励或值函数可获取。

## Extension to Robotics

在视觉-语言-动作（VLA）策略 refinement 中，环境奖励通常不可得。ARM 将奖励模型本身作为学习得到的 Critic，用相对优势 $\Delta G_t$ 替代显式环境优势，使 [[Advantage-Weighted-Behavior-Cloning|AW-BC]] 成为无需在线交互的离线策略改进实例。

## Related Concepts

- [[Offline-Reinforcement-Learning]] — 更广泛的离线 RL 范式
- [[Advantage-Estimation]] — 优势的定义与估计
- [[Advantage-Weighted-Behavior-Cloning]] — 机器人场景下的优势加权 BC
- [[Advantage-Reward-Modeling]] — 无需环境奖励的优势来源

## Papers

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]，第 2.2、3.4.3 节
- Peng et al., "Advantage-Weighted Regression: Simple and Scalable Off-Policy Reinforcement Learning", 2019
- Nair et al., "AWAC: Accelerating Online Reinforcement Learning with Offline Datasets", 2021
- Kostrikov et al., "Offline Reinforcement Learning with Implicit Q-Learning", 2021
