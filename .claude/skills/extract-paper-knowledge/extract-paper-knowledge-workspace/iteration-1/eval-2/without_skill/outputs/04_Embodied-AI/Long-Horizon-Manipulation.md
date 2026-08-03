---
title: "Long-Horizon Manipulation"
description: "需要多阶段、长时间、非单调执行序列的机器人操作任务，面临信用分配与数据质量挑战。"
tags: [embodied-ai, manipulation, robot-rl, long-horizon]
created: 2026-07-28
---

# Long-Horizon Manipulation

长程操作任务由多个相互依赖的阶段组成，常涉及变形物体、接触 rich 操作和非单调行为（如回退、重试、恢复）。

## 核心挑战

- 稀疏奖励难以提供有效学习信号。
- 人类演示中存在次优、噪声和非单调片段。
- 需要细粒度中间监督来引导信用分配。

## 典型任务

- 毛巾折叠（8 阶段：抓取、展平、多次折叠、放入盒子）
- 厨具整理、装配、家居整理等

## 关键方法

- [[Reward-Engineering-Bottleneck|奖励工程瓶颈]]
- [[Advantage-Reward-Modeling|优势奖励建模]]
- [[Advantage-Weighted-Behavior-Cloning|AW-BC]]
- 阶段感知奖励模型（如 SARM）

## 来源

- ARM: 第 1 节、第 4.1 节
