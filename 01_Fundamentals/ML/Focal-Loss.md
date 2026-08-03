---
title: Focal Loss
description: 通过降低易分样本权重来缓解类别不平衡问题的分类损失
tags:
  - ml
  - loss-function
  - classification
  - class-imbalance
  - fundamentals
created: 2026-07-28
---

# Focal Loss

在类别极度不平衡时，让模型更关注难分样本的损失函数。

## Why

标准交叉熵由大量易分样本主导，罕见但关键的样本（如长程操作轨迹中的成功终止帧）对梯度贡献不足。

## Core Idea

对预测概率 $p_t$ 的样本施加调制因子 $(1 - p_t)^\gamma$，降低高置信度易分样本的损失权重：

$$
\text{FL}(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)
$$

- $\gamma \geq 0$：聚焦参数，$\gamma$ 越大，易分样本权重衰减越厉害；
- $\alpha_t$：类别平衡权重。

## Usage in Robotics

在 [[Advantage-Reward-Modeling|ARM]] 中用于任务完成头（Completion Head），因为成功终止帧在长程连续轨迹中极为稀疏。

## Related Concepts

- [[Advantage-Reward-Modeling]] — 使用 Focal Loss 的奖励模型
- [[Long-Horizon-Manipulation-Reward]] — 长程操作奖励设计

## Papers

- Lin et al., "Focal Loss for Dense Object Detection", ICCV 2017
- [[arm]] — ARM: Advantage Reward Modeling for Long-Horizon Manipulation
