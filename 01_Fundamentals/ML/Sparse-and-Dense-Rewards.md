---
title: Sparse and Dense Rewards
description: 强化学习中两种基本奖励信号形式及其对长程任务学习的影响
tags:
  - ml
  - reinforcement-learning
  - reward-design
  - fundamentals
  - long-horizon
created: 2026-07-30
---

# Sparse and Dense Rewards

强化学习中奖励信号的两种基本形式：稀疏奖励仅在关键节点提供反馈，密集奖励在每一时间步提供连续监督。

## Sparse Reward

只在任务完成或失败时给出信号（如二值成功指示）。

- **优点**：标注简单，无需任务特定设计；
- **缺点**：在长程任务中信用分配困难，策略收敛慢；
- **典型场景**：围棋、最终状态可明确判定的任务。

## Dense Reward

在每个时间步或频繁给出连续信号，为策略提供持续引导。

- **优点**：缓解信用分配问题，训练更稳定；
- **缺点**：需要任务相关的启发式设计或精确进度模型，扩展性差；
- **典型问题**：非单调行为（回退、恢复）下易产生奖励错位。

## Trade-off in Long-Horizon Manipulation

长程机器人操作任务中：

- 稀疏奖励难以跨越多个子阶段；
- 密集奖励需要昂贵的 [[Reward-Engineering-Bottleneck|奖励工程]]；
- 替代方案是学习相对优势或任务完成锚点，以低成本提供高保真监督。

## Related Concepts

- [[Credit-Assignment]] — 稀疏奖励的核心困难
- [[Reward-Engineering-Bottleneck]] — 密集奖励的工程代价
- [[Advantage-Reward-Modeling]] — 用相对优势生成密集信号
- [[Reward-Shaping]] — 手动设计密集奖励的技术

## Papers

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]，第 1 节
