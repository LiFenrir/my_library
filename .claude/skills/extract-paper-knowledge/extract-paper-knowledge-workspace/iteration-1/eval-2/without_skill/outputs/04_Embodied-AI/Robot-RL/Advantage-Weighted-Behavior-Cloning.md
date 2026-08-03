---
title: "Advantage-Weighted Behavior Cloning"
description: "利用相对优势信号对行为克隆样本进行自适应加权，过滤次优轨迹并优先恢复行为。"
tags: [robot-rl, behavior-cloning, offline-rl, imitation-learning]
created: 2026-07-28
---

# Advantage-Weighted Behavior Cloning (AW-BC)

AW-BC 在 RA-BC 基础上引入长度自适应增益与统计归一化权重，使行为克隆能够从包含错误和恢复的异构数据中提取更优策略。

## 核心机制

- **长度自适应增益**: 对动作块 $H$ 内的进度差按序列长度归一化，消除不同长度轨迹的梯度差异。
  $$
  \Delta G_t = (P_{t+H} - P_t) \cdot \frac{L_{seq}}{\bar{L}}
  $$
- **统计权重**: 按批次均值和标准差裁剪，将增益映射到 $[0, 1]$ 的重要性权重。
- **加权负对数似然**: 高优势样本获得更大梯度，退步样本被抑制。

## 与离线 RL 的关系

形式上等价于 AWR 的思想：在接近行为策略的约束下最大化期望回报。ARM 充当学习的 Critic，提供优势估计。

## 来源

- ARM: 第 3.4 节
