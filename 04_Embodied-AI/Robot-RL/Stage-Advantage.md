---
title: Stage Advantage
description: 将长程任务分解为语义阶段，并直接估计阶段内状态对相对优势以降低训练信号方差
tags:
  - embodied-ai
  - robot-rl
  - advantage-estimation
  - long-horizon
  - concept
created: 2026-07-30
---

# Stage Advantage

Stage Advantage（SA）是一种用于长程机器人操作的 **阶段感知优势估计** 方法。它把长程任务分解为语义子目标（stage），并直接建模状态对之间的相对优势，以替代传统的值函数差分估计，从而获得更稳定、低方差的训练信号。

## Why

在长程任务中，用值函数差分估计优势的方法（如 $A(s,a) = V(s') - V(s)$）存在两个问题：

1. **数值不稳定**：两个独立预测的值相减会放大帧级估计噪声；
2. **多值歧义**：视觉上相似的状态可能出现在不同阶段，全局值函数会给出模糊的进度预测。

## Core Idea

将优势估计从“值函数差分”改为“直接预测”：

$$
A(s, a) = f_{\theta}(s, s')
$$

其中 $f_{\theta}$ 直接根据当前状态 $s$ 和下一状态 $s'$ 预测相对进度。为了避免对固定时间间隔过拟合，训练时随机采样时间跨度 $\Delta$，令 $s' = s_{t+\Delta}$。

进一步引入阶段条件：

$$
A_{\mathrm{stage}}(s, a, g) = f_{\theta}(s, s' \mid g)
$$

$g \in \{0, 1/S, \dots, (S-1)/S\}$ 为当前 stage 的归一化标量标签，$S$ 为阶段总数。这样优势只在同一语义阶段内评估，消除了多阶段任务中的多值歧义。

## Binary Optimality Indicator

参考 AWR 与 RECAP，将连续优势阈值化为二值最优性指示器：

$$
I = \mathbb{1}\left[ A_{\mathrm{stage}} > \epsilon \right]
$$

$\epsilon$ 为区分“有进展”与“无进展”的阈值。该指示器用于 advantage-weighted behavior cloning，对高优势样本加权。

## Comparison with Value-Difference Advantage

| 特性 | Value-Difference $V(s') - V(s)$ | Stage Advantage $f(s,s' \mid g)$ |
|---|---|---|
| 噪声 | 两个独立预测相减，方差高 | 单一预测，方差低 |
| 多阶段歧义 | 全局值函数多值 | 阶段条件消除歧义 |
| 训练目标 | 先学值函数再求差 | 直接以相对进度为目标 |
| 稳定性 | 容易抖动、收敛慢 | 更平滑，收敛更好 |

## Pros & Cons

- **优点**：
  - 显著降低优势训练信号的方差；
  - 阶段标签解决长程任务中的视觉-语义歧义；
  - 与 advantage-weighted BC / Flow-Matching VLA 兼容。
- **局限**：
  - 需要人工或启发式阶段标注；
  - 阶段设计对任务结构敏感；
  - 若任务本身无明显阶段，收益可能有限。

## Related Concepts

- [[Advantage-Weighted-Behavior-Cloning]] — SA 信号的下游用法
- [[Advantage-Reward-Modeling]] — 另一种相对优势建模思路
- [[RECAP]] — 使用值函数差分优势的 VLA 离线 RL 方法
- [[Distributional-Inconsistencies-in-Robot-Learning]] — SA 在 χ0 中的定位
- [[04_Embodied-AI/Robot-RL/long-horizon-manipulation|Long-Horizon-Manipulation]] — 问题背景

## Papers

- [[05_Papers/articles/chi0|χ0: Resource-Aware Robust Manipulation via Taming Distributional Inconsistencies]]
- Peng et al., "Advantage-weighted regression: Simple and scalable off-policy reinforcement learning", ICLR 2021
