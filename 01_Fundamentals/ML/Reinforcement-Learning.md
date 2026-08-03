---
title: "Reinforcement Learning"
description: "智能体通过与环境交互最大化累积奖励的序贯决策学习框架"
tags: [concept, fundamentals, ml, reinforcement-learning]
created: 2026-07-31
---

# Reinforcement Learning

**核心定义**：Reinforcement Learning（RL，强化学习）研究智能体如何在环境中通过试错学习策略，以最大化长期累积奖励。它形式化为马尔可夫决策过程（MDP）$
abla M = \langle S, A, P, R, \gamma \rangle$。

## 基本要素

| 符号 | 含义 |
|------|------|
| $S$ | 状态空间 |
| $A$ | 动作空间 |
| $P(s'|s,a)$ | 状态转移概率 |
| $R(s,a,s')$ | 奖励函数 |
| $\gamma$ | 折扣因子 |
| $\pi(a|s)$ | 策略 |
| $V^\pi(s)$ | 状态价值函数 |
| $Q^\pi(s,a)$ | 动作价值函数 |

## 核心问题

1. **策略学习**：直接学习 $\pi(a|s)$；
2. **价值估计**：学习 $V(s)$ 或 $Q(s,a)$ 来指导策略；
3. **探索与利用**：平衡尝试新动作与选择当前最优动作；
4. **信用分配**：将长期回报归因到具体状态-动作对。

## 主要方法族

- **基于价值**：Q-Learning、DQN、SAC
- **基于策略**：REINFORCE、PPO、TRPO
- **Actor-Critic**：A3C、SAC、TD3
- **基于模型**：Model-Based RL，先学环境动力学再规划
- **离线强化学习**：Offline RL，从固定数据集中学习

## 与其他概念的关系

- [[01_Fundamentals/ML/Reward-Shaping|Reward Shaping]] — 设计辅助奖励以加速学习
- [[01_Fundamentals/ML/Model-Based-Reinforcement-Learning|Model-Based Reinforcement Learning]] — 基于动力学模型的 RL
- [[01_Fundamentals/ML/Offline-Reinforcement-Learning|Offline Reinforcement Learning]] — 离线数据上的 RL
- [[01_Fundamentals/ML/Imitation-Learning|Imitation Learning]] — 从示范中学习，常与 RL 结合
- [[04_Embodied-AI/Robot-RL/Advantage-Conditioning|Advantage Conditioning]] — 用优势函数指导策略学习
