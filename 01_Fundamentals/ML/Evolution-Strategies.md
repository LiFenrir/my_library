---
title: "Evolution Strategies"
description: "通过维护并迭代一组参数解来优化策略的黑箱无梯度优化方法族。"
tags: [concept, ml, optimization, evolution-strategies, cma-es, policy-search]
created: 2026-07-28
---

# Evolution Strategies

进化策略（ES）是一类基于种群的黑箱优化方法，通过扰动参数、评估适应度、选择优秀个体来迭代搜索高适应度解，无需梯度。

## 核心流程

1. 初始化参数 $\theta$。
2. 生成 $N$ 个带噪声扰动的参数变体 $\theta_i = \theta + \epsilon_i$。
3. 在任务中评估每个变体的适应度（如累计奖励）。
4. 根据适应度更新 $\theta$。
5. 重复直到收敛。

## CMA-ES

协方差矩阵自适应进化策略（CMA-ES）是 ES 的重要实例，通过自适应调整搜索分布的均值与协方差矩阵，在参数空间较小（几千维）时表现优异。

## 在 World Model 中的应用

在 [[World-Model|World Model]] 中，控制器 $C$ 被设计为极小的线性模型（如 $a_t = W_c [z_t h_t] + b_c$），其参数可用 CMA-ES 直接优化。这种方法只需要最终累计奖励，易于并行 rollout。

## 优缺点

- 优点：不依赖梯度；对奖励稀疏或信用分配困难的任务鲁棒；高度并行化。
- 局限：高维参数空间效率低；超参数敏感；对模型结构可微性无要求但收敛可能慢于梯度方法。

## 相关概念

- [[World-Model]] — 用 CMA-ES 优化控制器的世界模型工作。
- [[Model-Based-Reinforcement-Learning|Model-Based RL]] — ES 可用于其中的策略搜索。

## 来源

- [[05_Papers/articles/world-models|World Models]]
