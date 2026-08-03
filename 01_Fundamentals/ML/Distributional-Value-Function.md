---
title: Distributional Value Function
description: 将状态值建模为价值分布而非单点期望的值函数表示
tags:
  - reinforcement-learning
  - value-function
  - distributional-rl
  - concept
created: 2026-07-28
---

# Distributional Value Function

不直接预测状态的标量值，而是预测未来回报在离散 bin 上的完整分布 $p_\phi(V | \mathbf{o}_t, \ell)$。

## Core Idea

将经验回报 $R_t(\tau) = \sum_{t'=t}^{\tilde{T}} r_{t'}$ 离散化为 $B$ 个 bin，用分类网络预测每个 bin 的概率：

$$
\min_\phi \mathbb{E}_{\tau \in \mathcal{D}} \left[ \sum_{\mathbf{o}_t \in \tau} H\left(R_t^B(\tau), \, p_\phi(V | \mathbf{o}_t, \ell)\right) \right]
$$

其中 $H$ 为交叉熵，$R_t^B$ 为离散化后的回报。

## Extracting Scalar Values

通过期望从分布中恢复连续值：

$$
V^{\pi_{\mathrm{ref}}}(\mathbf{o}_t, \ell) = \sum_{b \in [0,B]} p_\phi(V=b|\mathbf{o}_t, \ell) \, v(b)
$$

$v(b)$ 为 bin $b$ 对应的连续价值。

## Advantages

- 更稳定：避免自举目标中的过估计问题；交叉熵损失比 L2 回归更稳定。
- 更丰富的训练信号：整个分布提供额外监督。
- 捕获价值不确定性，便于提取分位数、优势等多样信号。
- 在 [[RECAP]] 中用于估计状态-动作优势，并判断动作是否优于参考策略。

## 在 RECAP 中的应用

π*0.6 用 distributional value function 预测"到成功完成的剩余步数"，并将值归一化到 $(-1, 0)$：

$$
r_t = \begin{cases} 0 & \text{if } t = T \text{ and success} \\ -C_{\text{fail}} & \text{if } t = T \text{ and failure} \\ -1 & \text{otherwise} \end{cases}
$$

## Related Concepts

- [[Advantage-Estimation]] — 从值函数提取优势
- [[RECAP]] — 用分布值函数训练 VLA 的值函数
- [[Offline-Reinforcement-Learning]] — 分布 RL 是离线价值学习的一种实现
- [[04_Embodied-AI/Robot-RL/Advantage-Conditioning|Advantage Conditioning]] — 从价值函数提取优势的策略提取方法

## 来源

- [[05_Papers/articles/pi-0-6|π*0.6: A VLA That Learns From Experience]]，第 IV-A 节
