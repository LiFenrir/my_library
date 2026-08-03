---
title: "模仿学习"
description: "从专家示范中学习策略，包含行为克隆与 DAgger 等数据聚合方法。"
tags: [concept, fundamentals, imitation-learning, behavior-cloning]
created: 2026-07-28
---

# 模仿学习

核心定义：不通过环境奖励，而是直接利用专家轨迹数据训练策略。

## 主要形式

- **行为克隆（Behavior Cloning, BC）**：将策略学习视为监督学习，最大化动作似然。
- **DAgger（Dataset Aggregation）**：通过在线滚动收集更多状态分布下的示范，修正复合误差。

## 优缺点

- 优点：实现简单、样本效率高（相对在线 RL）。
- 局限：对次优/噪声示范敏感，分布偏移会导致复合误差。

## 来源

- [[05_Papers/articles/arm|ARM]] — 对比了标准 BC、RA-BC 与 AW-BC 在长程毛巾折叠任务上的表现。
