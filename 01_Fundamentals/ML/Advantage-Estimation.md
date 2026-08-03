---
title: Advantage Estimation
description: 量化某个动作相对于当前策略期望水平的优劣程度
tags:
  - reinforcement-learning
  - advantage
  - policy-gradient
  - concept
created: 2026-07-28
---

# Advantage Estimation

优势函数 $A^\pi(\mathbf{o}_t, \mathbf{a}_t)$ 表示在状态 $\mathbf{o}_t$ 下采取动作 $\mathbf{a}_t$ 相对于策略 $\pi$ 平均表现的增益。

## Definition

$$
A^\pi(\mathbf{o}_t, \mathbf{a}_t) = \mathbb{E}_{\rho_\pi(\tau)}\left[\sum_{t'=t}^{t+N-1} r_{t'} + V^\pi(\mathbf{o}_{t+N})\right] - V^\pi(\mathbf{o}_t)
$$

- 前项为 $n$-step 动作值估计。
- 后项为当前状态值。
- 当 $N=T$ 时，退化为蒙特卡洛形式：$A = \sum_{t'=t}^{T} r_{t'} - V(\mathbf{o}_t)$。

## Usage

- **策略梯度**：作为动作好坏的权重，降低方差。
- **离线 RL**：AWR、CRR 用优势加权样本。
- **优势条件策略**：[[RECAP]] 将优势二值化为 "Advantage: positive/negative" 作为 VLA 输入。

## n-step Trade-off

- $N$ 小：偏差低，方差高。
- $N$ 大：利用值函数自举，方差低，但可能引入偏差。

## Related Concepts

- [[Distributional-Value-Function]] — 优势的来源之一
- [[Regularized-RL]] — 优势驱动的策略改进算子
- [[Advantage-Conditioning]] — 将优势作为条件输入的 VLA 训练方法
- [[RECAP]] — 在 VLA 中迭代使用优势估计
