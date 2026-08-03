---
title: Global Progress Reconstruction
description: 将 ARM 局部离散相对优势预测聚合为全局一致的密集进度曲线
tags:
  - embodied-ai
  - robot-rl
  - reward-model
  - arm
created: 2026-07-28
---

# Global Progress Reconstruction

把 [[Advantage-Reward-Modeling|ARM]] 在局部窗口内预测的离散相对优势积分成一条连续、全局一致的操作进度曲线。

## Why

相对优势只描述相邻状态之间的变化方向，无法直接作为下游策略的密集进度信号。需要把局部 $\Delta \hat{y}$ 转换为全局 $P_t \in [0, 1]$。

## How It Works

1. **并行推理**：利用 MIMO 架构一次处理非重叠视频片段，避免滑动窗口的冗余计算；
2. **序列对齐与填充**：末端片段不足窗口长度时复制末尾帧填充，聚合时丢弃填充对应预测；
3. **连续进度生成**：以任务完成头输出 $C_t$ 为锚点（如终止帧 $P_T = 1$），对相邻帧的优势预测 $\Delta \hat{y}$ 做累积，反推整条轨迹的密集进度值：

$$
P_t = P_{t+1} - \Delta \hat{y}_{t \to t+1}
$$

实际实现中结合完成锚点保证全局一致性，避免纯积分漂移。

## Properties

- 能刻画非单调进度（回退时出现下降“凹陷”）；
- 曲线平滑、密集，不依赖人工子任务边界；
- 为 [[Advantage-Weighted-Behavior-Cloning|AW-BC]] 提供稳定的训练权重来源。

## Related Concepts

- [[Advantage-Reward-Modeling]] — 提供局部优势预测
- [[Tri-state-Advantage-Labeling]] — 局部预测的训练信号
- [[Advantage-Weighted-Behavior-Cloning]] — 使用重建进度进行策略训练

## Papers

- [[arm]] — ARM: Advantage Reward Modeling for Long-Horizon Manipulation
