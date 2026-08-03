---
title: Tri-state Advantage Labeling
description: 用推进、回退、停滞三种离散相对优势标签降低长程操作奖励标注成本
tags:
  - embodied-ai
  - robot-rl
  - reward-model
  - annotation
  - arm
created: 2026-07-28
---

# Tri-state Advantage Labeling

将连续绝对进度标注替换为离散相对优势分类，以降低人工认知负荷并提高标注一致性。

## Why

传统方法要求标注者为每帧视频分配归一化进度 $P \in [0, 1]$：

- “进度”定义主观，标注者间一致性差；
- 认知负荷高，难以规模化；
- 绝对进度对回退、恢复等非单调行为刻画不足。

## Core Idea

对观测对 $(s_t, s_{t+k})$ 只判断相对变化方向，标签 $y \in \{ -1, 0, +1 \}$：

| 标签 | 含义 | 典型行为 |
|------|------|----------|
| $+1$ | Progressive（推进） | 有效朝向任务目标前进 |
| $0$ | Stagnant（停滞） | 等待、空闲、无实质进展 |
| $-1$ | Regressive（回退） | 偏离目标、出错、失败 |

## How It Works

1. **冷启动**：人工按三态规则标注少量数据；
2. **训练 [[Advantage-Reward-Modeling|ARM]]**：在三态标签上训练相对优势分类模型；
3. **自动标注**：用训练好的 ARM 对大量未标注轨迹推理，生成伪标签用于后续迭代。

该策略任务无关，对完整专家演示和碎片化 DAgger 数据均兼容。

## Related Concepts

- [[Advantage-Reward-Modeling]] — 使用三态标签的奖励模型
- [[Global-Progress-Reconstruction]] — 基于三态预测重建连续进度
- [[Long-Horizon-Manipulation-Reward]] — 长程操作奖励标注的通用问题

## Papers

- [[arm]] — ARM: Advantage Reward Modeling for Long-Horizon Manipulation
