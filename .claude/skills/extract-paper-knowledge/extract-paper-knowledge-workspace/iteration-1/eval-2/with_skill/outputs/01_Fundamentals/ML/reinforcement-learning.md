---
title: "强化学习基础"
description: "智能体通过与环境交互学习策略，以最大化累积回报；在长程操纵中面临稀疏奖励与信用分配问题。"
tags: [concept, fundamentals, rl, credit-assignment]
created: 2026-07-28
---

# 强化学习基础

核心定义：通过试错与环境交互，学习一个将状态映射到动作的策略，使得长期累积奖励最大。

## 关键问题

- **稀疏奖励（sparse rewards）**：只在任务完成时给出二值信号，难以指导长程任务学习。
- **密集奖励（dense rewards）**：提供连续进度信号，但设计成本高且容易引入偏差。
- **信用分配（credit assignment）**：需要判断长序列中哪些动作对最终成功有贡献。
- **奖励工程瓶颈**：手工设计奖励函数耗时、任务相关，且在不结构化环境中难以扩展。

## 相关方法

- [[inverse-reinforcement-learning|逆强化学习（IRL）]] — 从示范中推断奖励函数。
- [[rlhf|RLHF]] — 从人类反馈中学习奖励模型。
- [[reward-shaping|奖励塑形]] — 在不改变最优策略的前提下引入启发式信号。

## 来源

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]
