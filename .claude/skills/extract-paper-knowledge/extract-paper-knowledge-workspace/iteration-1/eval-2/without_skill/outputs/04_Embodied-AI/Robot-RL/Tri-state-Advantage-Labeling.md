---
title: "Tri-state Advantage Labeling"
description: "用 +1 / 0 / -1 三种离散标签标注相对优势，降低人工成本并支持自动伪标签。"
tags: [robot-rl, annotation, reward-model]
created: 2026-07-28
---

# Tri-state Advantage Labeling

将奖励标注从连续进度值（如 $P \in [0, 1]$）简化为三分类任务，显著降低认知负荷并提高标注一致性。

## 标签定义

- **+1 (Progressing)**: 状态有效向目标推进。
- **0 (Stagnant)**: 无明显进展，如等待、空闲。
- **-1 (Regressing)**: 状态偏离目标、出错或失败。

## 优点

- 任务无关，跨任务一致。
- 兼容异构、碎片化数据（如 DAgger 增强的错误纠正片段）。
- 训练后的模型可用于自动标注未标注轨迹，扩展为大规模伪标签数据。

## 效率

- 人类三元标注：约 250 样本 / 8 小时。
- 自动三元标注：> 400,000 样本 / 8 小时（A100）。

## 来源

- ARM: 第 3.2.2 节、第 4.3 节
