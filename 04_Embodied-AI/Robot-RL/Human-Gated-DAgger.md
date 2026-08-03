---
title: Human-Gated DAgger
description: 在自主执行过程中由专家介入并提供纠正性示例的模仿/强化学习数据收集方式
tags:
  - embodied-ai
  - robot-rl
  - imitation-learning
  - concept
created: 2026-07-28
---

# Human-Gated DAgger

在机器人自主运行期间，人类专家监控系统并在必要时接管或纠正，从而生成高质量的纠正性轨迹数据。

## Core Idea

源自 DAgger（Dataset Aggregation）系列：不仅用初始演示训练策略，还让策略在实际分布中执行，由专家标注或纠正错误动作，逐步扩大数据集覆盖的状态分布。

在 Human-Gated DAgger 中，专家可以选择：
- 完全自主运行；
- 在关键失败点接管并纠正；
- 纠正后的动作被记录为 positive 示例。

## Role in RL

在 [[RECAP]] 中，人类干预不是唯一的监督来源，而是与自主经验结合：

- 纠正动作强制标记为 $I_t = \mathrm{True}$（高优势）。
- 整个 episode（包括自主段和纠正段）都加入数据集。
- 纠正主要用于修复灾难性失败和辅助探索，而非提供完整最优监督。

## Limitations

- 人类无法保证每次干预质量一致。
- 频繁干预会改变状态分布，导致纠正动作未必适用于纯自主场景。
- 难以通过干预优化行为细节（如整体速度、流畅度）。

## Related Concepts

- [[RECAP]] — 将 Human-Gated DAgger 与离线 RL 结合的方法
- [[Offline-RL-for-VLA]] — 异构数据（含纠正）的统一训练框架
- [[Advantage-Conditioning]] — 纠正动作被强制标记为 positive 的机制
