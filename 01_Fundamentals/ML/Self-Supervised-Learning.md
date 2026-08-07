---
title: Self-Supervised Learning
description: 通过捕捉输入各部分之间依赖关系来学习表示的范式，核心可归结为模式补全
tags:
  - concept
  - ml
  - self-supervised-learning
  - representation-learning
  - energy-based-model
created: 2026-07-30
---

# Self-Supervised Learning

Self-Supervised Learning（SSL）是一种让学习系统捕捉输入各部分之间相互依赖的范式。具体实现通常是“模式补全”：给定输入的一部分 $x$，判断对缺失部分 $y$ 的补全是否一致/合理。

## 核心思想

- 不直接要求模型从 $x$ 生成 $y$。
- 训练模型判断 $x$ 与候选 $y$ 是否兼容。
- 由于一个 $x$ 可能对应多个合理的 $y$（如视频的多种未来），SSL 天然适合多模态建模。

## 通用框架

用 [[Energy-Based-Model|EBM]] 形式化：

$$
F_w(x, y)
$$

- $x$：已观测部分（如过去视频片段）。
- $y$：待补全部分（如未来视频片段）。
- $F_w(x, y)$ 低表示兼容，高表示不兼容。

## 学习目标

给定 $x$ 和 $y$，学习编码器：

$$
s_x = g_x(x), \quad s_y = g_y(y)
$$

使得：

1. $s_x$ 对 $x$ 信息量最大。
2. $s_y$ 对 $y$ 信息量最大。
3. $s_y$ 能从 $s_x$ 容易地预测。

这一 trade-off 让模型学到“既信息丰富又可预测”的表示。

## 从预测中学习抽象概念

在视频上训练 SSL 时，系统可能自发学习层次化概念：

- 局部边缘、轮廓与运动。
- 深度图（因为一个视角可由邻近视角预测）。
- 物体、遮挡、物体恒存性。
- 无生命/有生命物体的区分。
- 直观物理：稳定性、重力、惯性等。

## 训练策略

- **对比方法**：构造负样本 $\hat{y}$，损失拉低正样本能量、拉高负样本能量。
- **正则化方法**：不依赖负样本，通过限制低能量区域体积防止崩塌。

## 与其他概念的关系

- [[Energy-Based-Model|EBM]] — SSL 的统一数学框架。
- [[Joint-Embedding-Predictive-Architecture|JEPA]] — 非生成式 SSL 架构，用于学习世界模型。
- [[VICReg]] — 非样本对比的 SSL 方法，可用于训练 JEPA。

## 来源

- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]，LeCun，2022
