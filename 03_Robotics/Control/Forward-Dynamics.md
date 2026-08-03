---
title: Forward Dynamics
description: 给定当前状态与动作，预测下一状态或观测的环境动力学模型
tags:
  - robotics
  - control
  - dynamics
  - world-model
  - manipulation
created: 2026-07-30
---

# Forward Dynamics

**Forward Dynamics（正向动力学）** 指根据当前状态与执行的动作，预测环境或机器人下一时刻状态/观测的模型。

## Core Idea

与 **Inverse Dynamics** 相对：

- **正向动力学**：$s_{t+1} \sim p(\cdot \mid s_t, a_t)$，给定动作预测下一状态；
- **逆动力学**：$a_t \sim g(\cdot \mid s_t, s_{t+1})$，给定状态转移反推动作。

在视觉-动作学习中，正向动力学常用潜在状态表示：

$$
\hat{z}_{t+1} \sim p_\theta(\cdot \mid z_t, a_t, z_{<t}, a_{<t})
$$

其中 $z_t$ 为视觉 VAE 隐状态，$a_t$ 为动作。

## In Robotics

正向动力学模型在机器人控制中有多种用途：

- **MPC 与规划**：在想象中推演动作后果，选择最优动作序列；
- **仿真器替代**：作为可微分世界模型，支持策略在模型中训练；
- **异步推理接地**：在异步控制管道中，用最新真实观测 $z_{t-1}$ 和正在执行的动作 $a_t$ 重新生成当前时刻预测 $\hat{z}_t$，避免依赖陈旧预测导致开环漂移。

## 与逆动力学的协作

典型解耦范式：

1. **正向动力学** 预测未来视觉状态；
2. **逆动力学** 根据预测的视觉转移解码可执行动作。

两者结合构成 "想象-执行" 闭环。

## 优缺点

- **优点**：
  - 显式建模物理演化，可解释性强；
  - 支持规划与反事实推演；
  - 可用于异步推理中重新对齐真实反馈。
- **缺点/局限**：
  - 多步预测误差会复合；
  - 对分布外状态容易退化；
  - 需要足够的数据学习接触动力学等复杂物理。

## Related Concepts

- [[03_Robotics/Control/Inverse-Dynamics|Inverse Dynamics]] — 从状态转移反推动作
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 使用正向/逆动力学统一视频-动作建模
- [[01_Fundamentals/ML/Model-Based-Reinforcement-Learning|Model-Based Reinforcement Learning]] — 正向动力学是核心组件
- [[04_Embodied-AI/World-Model/World-Model|World Model]] — 学习环境的内部预测模型

## Papers

- [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]] — 用 FDM 在异步推理中接地真实观测
