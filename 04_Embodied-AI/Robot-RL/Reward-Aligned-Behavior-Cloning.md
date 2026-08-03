---
title: Reward-Aligned Behavior Cloning
description: 用阶段感知奖励模型而非环境奖励对行为克隆样本加权的机器人模仿学习方法
tags:
  - embodied-ai
  - robot-rl
  - imitation-learning
  - offline-rl
  - behavior-cloning
  - sarm
  - ra-bc
created: 2026-07-30
---

# Reward-Aligned Behavior Cloning (RA-BC)

通过阶段感知（stage-aware）奖励模型对行为克隆样本进行加权，从而从含噪声的次优演示中筛选高质量片段的离线学习范式。

## Why

标准行为克隆平等对待所有样本，难以处理真实演示中的错误、迟疑和重复尝试。传统优势加权方法（如 AWR、AWAC、IQL）需要环境奖励来拟合全局值函数，而在视觉驱动的真实机器人场景中环境奖励通常不可得。

## Core Idea

用学习得到的阶段级奖励模型替代环境奖励，根据子任务完成度或阶段进度为每个样本分配权重：

- 高奖励样本获得更高训练权重；
- 低奖励或错误样本被抑制；
- 无需在线交互，仅依赖离线演示数据。

SARM 提出的 RA-BC 是该范式的代表：利用人工语言子任务标注定义阶段边界，训练阶段感知奖励模型并据此重加权行为克隆。

## Limitations

- 依赖昂贵的人工语言子任务标注；
- 粗粒度子任务分段难以捕捉阶段内的恢复、纠正等关键转换；
- 基于绝对进度的阶段定义假设单调性，难以刻画回退行为。

## Relation to ARM

ARM 将 RA-BC 中的阶段级绝对进度替换为相对优势，并进一步提出 [[Advantage-Weighted-Behavior-Cloning|AW-BC]]：

- 用三态相对优势标签替代人工子任务标注；
- 用 MIMO 时序 Transformer 提供密集、非单调的优势信号；
- 引入长度自适应增益和统计归一化，兼容碎片化 DAgger 数据。

## Related Concepts

- [[Advantage-Weighted-Behavior-Cloning]] — ARM 提出的改进加权行为克隆
- [[Advantage-Reward-Modeling]] — 为 AW-BC 提供优势信号的模型
- [[Imitation-Learning]] — 基础范式
- [[Offline-Reinforcement-Learning]] — 方法论归属
- [[Long-Horizon-Manipulation-Reward]] — 问题背景

## Papers

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]，第 2.2 节
- SARM: Stage-aware Reward Modeling for Long Horizon Robot Manipulation
