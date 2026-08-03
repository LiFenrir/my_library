---
title: Mode-1 / Mode-2 Reasoning
description: 自主智能体中反应性行为与基于世界模型的推理规划两种决策模式
tags:
  - concept
  - ai
  - cognitive-architecture
  - reasoning
  - planning
  - system-1-system-2
created: 2026-07-30
---

# Mode-1 / Mode-2 Reasoning

在 LeCun 的自主智能体架构中，感知-行动循环分为两种模式，分别对应 Kahneman 的 System 1 与 System 2。

## Mode-1：反应性行为

- 感知模块编码当前状态 $s[0] = \operatorname{Enc}(x)$。
- 策略模块直接输出动作 $a[0] = A(s[0])$。
- 不涉及显式世界模型模拟或规划。
- 可并行运行多个专门化策略网络。

### 关键限制

外部世界不可微，无法将成本梯度直接反向传播到动作。Mode-1 的策略更新通常依赖策略梯度方法，需要在真实环境中尝试多个扰动动作，样本效率低且可能危险。

## Mode-2：推理与规划

使用 World Model 进行多步模拟，并通过成本模块优化动作序列：

1. **感知**：$s[0] = P(x)$。
2. **动作提议**：Actor 提出候选动作序列 $(a[0], \dots, a[T])$。
3. **模拟**：World Model 递归预测状态序列：

$$
s[t+1] = \operatorname{Pred}(s[t], a[t])
$$

4. **评估**：计算总能量/成本：

$$
F(x) = \sum_{t=1}^{T} C(s[t])
$$

5. **规划**：通过梯度下降或其他优化方法更新动作序列，最小化总成本。
6. **执行**：输出优化后动作序列的第一个动作。
7. **记忆**：将状态-成本对存入短期记忆，用于训练 Critic。

### 本质

Mode-2 是模型预测控制（[[Model-Predictive-Control|MPC]]）的可学习版本，其中世界模型和成本函数均由学习得到。

## 从 Mode-2 到 Mode-1：技能编译

Mode-2 代价高昂，因为 World Model 是稀缺资源。智能体可以通过“蒸馏”把 Mode-2 的规划能力编译为 Mode-1 的快速反应策略：

$$
\min D(\check{a}[t], A(s[t]))
$$

训练后的策略网络 $A$ 可以：

- 单独用于快速反应。
- 为 Mode-2 提供好的初始动作序列，加速优化。

## 推理即能量最小化

Mode-2 中的规划可视为约束满足或能量最小化。许多经典 AI 推理形式（概率图模型、因子图）都可纳入这一框架。该架构中的成本模块可看作因子图中的对数因子。

## 与其他概念的关系

- [[Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]] — 包含 Mode-1/Mode-2 的整体架构。
- [[Model-Predictive-Control|MPC]] — Mode-2 的理论基础。
- [[Energy-Based-Model|EBM]] — 推理可表述为能量最小化。
- [[Joint-Embedding-Predictive-Architecture|JEPA]] — Mode-2 中使用的世界模型架构。

## 来源

- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards Autonomous Machine Intelligence]]，LeCun，2022
