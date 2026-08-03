---
title: "Advantage Reward Modeling"
description: "通过多帧多输出 Transformer 估计轨迹片段的相对优势，替代绝对进度奖励建模。"
tags: [robot-rl, reward-model, advantage, imitation-learning]
created: 2026-07-28
---

# Advantage Reward Modeling (ARM)

ARM 将奖励建模从“绝对进度回归”转向“相对优势分类”。通过比较历史观测与当前观测，判断状态转移是进步、退步还是停滞。

## 核心组件

- **MIMO Temporal Transformer**: 同时输入多个历史帧，输出多个帧间优势预测。
- **双头目标**:
  - 帧间优势分类：输出 +1 / 0 / -1。
  - 任务完成预测：用 Focal Loss 处理类别不平衡，提供全局进度锚点。
- **全局进度重建**: 将局部相对预测与完成锚点结合，生成平滑密集进度曲线。

## 输入模态

- CLIP 视觉特征
- 机器人本体感受状态
- 任务语言指令

## 来源

- ARM: 第 3.2-3.3 节
