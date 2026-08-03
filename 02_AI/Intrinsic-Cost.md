---
title: Intrinsic Cost
description: 自主智能体中不可训练的基础成本模块，定义基本驱动力与安全护栏
tags:
  - concept
  - ai
  - autonomous-agent
  - intrinsic-motivation
  - reinforcement-learning
  - safety
created: 2026-07-30
---

# Intrinsic Cost

Intrinsic Cost（内在成本）是自主智能体成本模块中**不可训练**的子模块，用于度量当前状态的即时“不适度”。它是智能体基本行为的来源，决定其本能驱动力与价值观。

## 核心特性

- **不可变**：不允许通过梯度学习或外部修改，防止行为漂移或崩溃。
- **标量输出**：输出一个能量值，高能量表示不适（疼痛、危险），低/负能量表示舒适（满足、愉悦）。
- **可被配置器调制**：在不同任务中可调整各子项的权重，但子项本身不变。

## 成本模块组成

$$
C(s) = \operatorname{IC}(s) + \operatorname{TC}(s)
$$

- $\operatorname{IC}(s)$：Intrinsic Cost，即时内在成本。
- $\operatorname{TC}(s)$：Trainable Critic，预测未来内在成本。

Intrinsic Cost 通常是多个子模块的线性组合：

$$
\operatorname{IC}(s) = \sum_{i=1}^{k} u_i \operatorname{IC}_i(s)
$$

权重 $u_i$ 由 Configurator 根据任务调制。

## 典型内在驱动示例

### 机器人

- 外部力过载、危险电气/化学/热环境。
- 能量储备过低。
- 过度功耗。

### 一般智能体

- 站立、行走等基础运动驱动力。
- 对人类陪伴与互动的社交倾向。
- 观察到他人痛苦时的不适（类共情）。
- 好奇心：面对新情境时获得低能量，驱动探索。
- 能动性：影响世界状态获得奖励。

## 与 Critic 的关系

- Intrinsic Cost 评估**即时**状态。
- Trainable Critic 预测**未来**内在成本，使智能体能够做长期规划。
- Critic 通过短期记忆中的 (state, intrinsic cost) 对进行训练。

## 为什么必须不可训练

如果 Intrinsic Cost 可学习，智能体可能找到“作弊”方式降低能量，而不是真正解决任务或避免危险。例如：

- 关闭疼痛传感器。
- 忽视安全约束。

因此，IC 作为硬编码的价值观底座，是自主智能体安全性的关键设计。

## 与其他概念的关系

- [[Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]] — Intrinsic Cost 是该架构的成本模块子组件。
- [[Model-Predictive-Control|MPC]] — 规划目标是最小化由 IC 与 Critic 构成的总成本。
- [[Mode-1-Mode-2-Reasoning|Mode-1 / Mode-2]] — Mode-2 规划以最小化长期成本为目标。

## 来源

- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards Autonomous Machine Intelligence]]，LeCun，2022
