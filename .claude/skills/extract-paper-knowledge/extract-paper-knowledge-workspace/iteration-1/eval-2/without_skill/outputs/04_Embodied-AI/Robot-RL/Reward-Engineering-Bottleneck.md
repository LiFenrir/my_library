---
title: "Reward Engineering Bottleneck"
description: "长程机器人操作中奖励设计依赖密集进度标注或环境奖励，导致可扩展性与稳定性受限。"
tags: [robot-rl, reward-design, long-horizon]
created: 2026-07-28
---

# Reward Engineering Bottleneck

长程机器人操作的 RL/离线 RL 需要信息丰富的奖励信号。稀疏奖励难以做信用分配，而密集奖励又依赖人工进度模型或环境奖励，成本高且难以泛化。

## 瓶颈来源

- 零样本 VLM 标注不稳定、成本高、缺乏空间几何 grounding。
- 绝对进度模型常假设单调性，无法处理回退、重试、恢复行为。
- 粗粒度子任务分段难以捕捉阶段内关键过渡。

## 缓解思路

- 用相对优势替代绝对进度，减少对任务特定启发式的依赖。
- 用低成本三元状态标注（进步/退步/停滞）启动奖励模型。

## 来源

- ARM: 第 1-2 节
