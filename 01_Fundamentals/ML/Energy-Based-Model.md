---
title: Energy-Based Model
description: 用标量能量函数刻画变量间兼容性的非概率化建模框架
tags:
  - concept
  - ml
  - energy-based-model
  - self-supervised-learning
  - latent-variable-model
created: 2026-07-30
---

# Energy-Based Model

Energy-Based Model（EBM）将学习系统定义为一个标量能量函数 $F_w(x, y)$：当输入 $x$ 与候选 $y$ 兼容时输出低能量，不兼容时输出高能量。与概率模型不同，EBM 把能量函数本身视为基本对象，不必通过 Gibbs 分布归一化。

## 为什么需要 EBM

- 很多学习任务本质是判断“哪些 $y$ 与 $x$ 兼容”，而非显式生成 $y$。
- 当存在多个兼容 $y$ 时（如视频后续的多模态未来），生成式模型需要表示无穷集合；EBM 只需判断某个候选是否兼容。
- 为 [[Self-Supervised-Learning|SSL]]、[[Joint-Embedding-Predictive-Architecture|JEPA]] 和分层世界模型提供统一数学框架。

## 核心形式

给定观测部分 $x$ 与待补全部分 $y$，学习能量函数：

$$
F_w(x, y) \in \mathbb{R}
$$

- 训练样本 $(x, y)$：能量低。
- 非样本 $\hat{y} \neq y$：能量高。

### 隐变量 EBM（LVEBM）

当 $y$ 无法仅由 $x$ 确定时，引入隐变量 $z$ 参数化兼容关系：

$$
\check{z} = \underset{z \in \mathcal{Z}}{\operatorname{argmin}} E_w(x, y, z)
$$

$$
F_w(x, y) = \min_{z \in \mathcal{Z}} E_w(x, y, z)
$$

$z$ 表示 $y$ 中无法从 $x$ 提取、但对预测有用的信息。

## 训练方法

训练 EBM 需同时满足两点：

1. 训练样本能量低。
2. 非训练区域能量高，防止能量崩塌（collapse）。

### 对比方法

用损失把训练样本能量拉低、把构造的负样本能量拉高。常见损失：

- 成对 hinge 损失：

$$
L(w, x, y, \hat{y}) = \left[ F_w(x, y) - F_w(x, \hat{y}) + \mu \|y - \hat{y}\|^2 \right]^+
$$

- InfoNCE：

$$
L = F_w(x, y) + \log \left[ \exp(-F_w(x, y)) + \sum_{k=1}^{K} \exp(-F_w(x, \hat{y}[k])) \right]
$$

**问题**：高维 $y$ 空间中，负样本数可能随维度指数增长，导致维度灾难。

### 正则化方法

不依赖负样本，而是对低能量区域体积进行正则化，使能量面“收缩包裹”数据流形：

- 限制隐变量 $z$ 的信息容量（离散、低维、稀疏、噪声）。
- 最大化编码器输出的信息量，防止表示崩塌。
- 例子：稀疏建模、VAE、VQ-VAE、隐式秩最小化自编码器。

## 典型架构的崩塌风险

| 架构 | 是否会崩塌 | 原因 |
|------|------------|------|
| 确定性生成架构 | 否 | 每个 $x$ 只产生单一 $\tilde{y}$ |
| 非确定性生成架构 | 是 | 隐变量容量过大时可能覆盖整个 $y$ 空间 |
| 自编码器 | 是 | 表示维度足够高时可学会恒等映射 |
| 联合嵌入架构 | 是 | 编码器可能忽略输入并输出常数 |

## 与其他概念的关系

- [[Self-Supervised-Learning|SSL]] — EBM 是 SSL 的统一数学框架。
- [[Joint-Embedding-Predictive-Architecture|JEPA]] — JEPA 是一种非生成式 EBM，能量为表示空间中的预测误差。
- [[Variational-Autoencoder|VAE]] — 可看作带概率解释的正则化 EBM。
- [[Model-Based-Reinforcement-Learning|Model-Based RL]] — 世界模型可建模为 EBM，用能量刻画状态转移的合理性。

## 来源

- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]，LeCun，2022
