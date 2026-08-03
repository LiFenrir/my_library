---
title: "RL Token"
description: "从冻结 VLA 中提取紧凑表示作为轻量级在线 RL actor-critic 状态接口的方法"
tags: [concept, embodied-ai, vla, robot-rl]
created: 2026-07-29
---

# RL Token

**核心定义**：RL Token 是一种从冻结的预训练 VLA 中提取紧凑表示（readout embedding）的方法，作为轻量级在线强化学习 actor-critic 的状态输入，从而在保留 VLA 先验的同时实现样本高效的在线适应。

## 动机

- 直接对整个 VLA 进行在线 RL 更新：计算昂贵、样本低效
- 完全从头训练小策略：放弃 VLA 的丰富感知和行为先验
- RL Token 在两者之间取得平衡：冻结 VLA 提供表示，小网络进行在线学习

## 提取方式

在 VLA 最后一层 token 嵌入序列 $\mathbf{z}_{1:M}$ 后追加一个可学习的 special token $\mathbf{e}_{\mathrm{rl}}$，通过一个轻量 encoder transformer $g_\phi$ 处理：

$$
\mathbf{z}_{\mathrm{rl}} = g_\phi\left(\left[ \mathbf{z}_{1:M}, \mathbf{e}_{\mathrm{rl}} \right]\right)_{M+1}
$$

该位置的输出即为 RL token。

为了让 RL token 保留足够信息，训练一个 decoder transformer 从 $\mathbf{z}_{\mathrm{rl}}$ 自回归重建原始 VLA 嵌入：

$$
\mathcal{L}_{\mathrm{ro}} = \mathbb{E}_{\mathcal{D}} \left[ \sum_{i=1}^{M} \left\| h_\phi\left(d_\phi\left(\left[ \mathbf{z}_{\mathrm{rl}}, \bar{\mathbf{z}}_{1:i-1} \right]\right)\right)_i - \bar{\mathbf{z}}_i \right\|^2 \right]
$$

其中 $\bar{\mathbf{z}}_i = \mathrm{sg}(\mathbf{z}_i)$ 为 stop-gradient 的 VLA 嵌入。

## 在线 RL 使用

- 冻结 VLA 和 RL token 提取器
- 训练轻量级 actor 和 critic
- Actor 以 VLA 参考动作块为条件，并正则化保持接近 VLA 行为
- Critic 估计状态-动作块价值

## 优缺点

- **优点**：
  - 保留 VLA 预训练先验
  - 在线 RL 网络小，样本高效
  - 可以在几小时内提升任务成功率和执行速度
- **缺点/局限**：
  - 需要任务特定演示数据训练 RL token
  - 行为受 VLA 先验约束

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — RL Token 的信息来源
- [[04_Embodied-AI/Robot-RL/RECAP|RECAP]] — 另一种 VLA + RL 的训练框架
- [[04_Embodied-AI/Robot-RL/Advantage-Conditioning|Advantage Conditioning]] — 不同方式的 VLA + RL

## 来源

- [[05_Papers/articles/rl-token-bootstrapping|RL Token: Bootstrapping Online RL with Vision-Language-Action Models]]，第 IV-A 节
