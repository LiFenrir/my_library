---
title: Credit Assignment
description: 强化学习中将最终回报归因于个体动作或状态-动作对的困难
tags:
  - ml
  - reinforcement-learning
  - credit-assignment
  - fundamentals
  - long-horizon
created: 2026-07-30
---

# Credit Assignment

在序列决策中，判断哪些动作或状态转移对最终成功/失败负责的问题。

## Why It Matters

- 长程任务中单个动作的影响可能延迟多步才能显现；
- 稀疏奖励只给出最终结果，难以区分关键动作与无关动作；
- 错误的信用归因会导致策略更新方向错误。

## Common Solutions

1. **Dense Rewards**：提供更频繁的反馈，缩小信用归因范围；
2. **Advantage Estimation**：量化某个动作相对于当前策略期望水平的增益；
3. **Value Functions**：估计状态或状态-动作对的长期回报；
4. **Reward Shaping**：通过领域知识设计引导性奖励。

## In Long-Horizon Manipulation

机器人操作任务中，信用分配尤为困难：

- 动作空间高维且连续；
- 视觉观测部分可观测；
- 物体形变、接触动力学复杂。

ARM 通过相对优势建模将信用分配问题转化为局部分类：只需判断相邻状态间是推进、停滞还是回退，无需精确的全局进度函数。

## Related Concepts

- [[Sparse-and-Dense-Rewards]] — 奖励频率对信用分配的影响
- [[Advantage-Estimation]] — 量化动作相对价值
- [[Advantage-Reward-Modeling]] — 用相对优势简化信用分配
- [[Offline-Reinforcement-Learning]] — 从离线数据中学习值函数

## Papers

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]，第 1 节
