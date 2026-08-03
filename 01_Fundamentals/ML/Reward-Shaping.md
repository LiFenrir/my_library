---
title: "Reward Shaping"
description: "通过设计辅助奖励函数引导强化学习智能体更快学习且不改变最优策略的技术"
tags: [concept, fundamentals, ml, reinforcement-learning]
created: 2026-07-30
---

# Reward Shaping

**核心定义**：Reward Shaping 是在强化学习中设计辅助奖励函数 $F(s, a, s')$ 与原奖励 $R$ 相加，以提供额外学习信号、加速收敛的技术。理想情况下不应改变最优策略。

## 形式化

塑形后的奖励：

$$
R'(s, a, s') = R(s, a, s') + F(s, a, s')
$$

## 电位式 Reward Shaping

Ng, Harada & Russell (1999) 证明：若 $F(s, a, s') = \gamma \Phi(s') - \Phi(s)$，其中 $\Phi$ 为电位函数，则最优策略不变。

## 应用

- 长程任务中提供中间进度信号；
- 机器人操作中的子目标奖励；
- 稀疏奖励环境的密集化。

## 风险

- 设计不当会改变最优策略；
- 可能鼓励奖励 hacking。

## 与其他概念的关系

- [[01_Fundamentals/ML/Sparse-and-Dense-Rewards|Sparse and Dense Rewards]] — Reward Shaping 处理的核心问题
- [[01_Fundamentals/ML/Reinforcement-Learning|Reinforcement Learning]] — 应用场景

## 来源

- Ng, Harada & Russell, 1999, "Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping"
