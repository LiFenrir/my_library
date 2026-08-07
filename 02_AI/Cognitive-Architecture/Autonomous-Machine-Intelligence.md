---
title: Autonomous Machine Intelligence
description: LeCun 提出的全可微认知架构，通过世界模型、成本模块与演员模块实现自主推理与规划
tags:
  - concept
  - ai
  - cognitive-architecture
  - autonomous-agent
  - world-model
  - intrinsic-motivation
created: 2026-07-30
---

# Autonomous Machine Intelligence

Autonomous Machine Intelligence 是 LeCun 在 2022 年提出的一种自主智能体认知架构。其核心目标是让机器像动物和人类一样，通过观察学习世界模型，并基于内在动机进行推理、规划和行动。

## 核心问题

当前 AI 与人类学习能力的差距主要体现在三方面：

1. 如何主要通过观察学习世界表示、预测和行动？
2. 如何以与梯度学习兼容的方式进行推理和规划？
3. 如何在多个抽象层次和时间尺度上学习表示和行动计划？

## 整体架构

架构由六个全可微模块组成，所有模块均可通过成本模块反向传播梯度：

| 模块 | 功能 |
|------|------|
| **Configurator** | 接收任务描述，配置其他模块的参数与注意力 |
| **Perception** | 从传感器估计当前世界状态 |
| **World Model** | 补全缺失信息，预测未来状态 |
| **Cost** | 计算标量“不适度”能量，驱动行为 |
| **Short-Term Memory** | 存储当前与预测的状态及成本 |
| **Actor** | 提出并优化动作序列 |

## 成本模块

成本模块是行为的唯一驱动器，由两部分组成：

$$
C(s) = \operatorname{IC}(s) + \operatorname{TC}(s)
$$

- **Intrinsic Cost（IC）**：不可训练，定义基本驱动力，如疼痛、饥饿、好奇心、社交倾向等。
- **Trainable Critic（TC）**：可训练，预测未来内在成本，使智能体能做长期规划。

IC 与 TC 都可能是多个子模块的线性组合，权重由 configurator 调制以关注不同子目标。

## 两种行为模式

### Mode-1：反应性行为

类似 Kahneman 的 System 1：感知 → 策略模块 → 动作，无需显式规划。

### Mode-2：推理与规划

类似 System 2：通过 World Model 模拟动作序列的未来结果，并在表示空间中优化动作序列以最小化总成本。本质上是可学习版本的 [[Model-Predictive-Control|MPC]]。

## 从 Mode-2 到 Mode-1 的技能编译

Mode-2 计算代价高且串行，一次只能处理一个复杂任务。智能体可让 Mode-2 产生最优动作序列，再用这些序列训练一个 Mode-1 策略网络 $A(s[t])$：

$$
\min D(\check{a}[t], A(s[t]))
$$

训练好的策略网络可快速反应，也可作为 Mode-2 优化的初始动作序列。

## 行为定义方式

按工程复杂度从低到高：

1. 显式编程行为。
2. 设计目标函数，让智能体自行优化动作。
3. 直接监督模仿专家动作。
4. 逆强化学习：从专家行为推断成本函数。

其中第 2 种（目标函数）最鲁棒，因为智能体可适应意外环境变化。

## 与其他概念的关系

- [[World-Model]] — 架构的核心模块，由 [[Joint-Embedding-Predictive-Architecture|JEPA]] / [[Hierarchical-JEPA|H-JEPA]] 实现。
- [[Model-Predictive-Control|MPC]] — Mode-2 规划的理论基础。
- [[Energy-Based-Model|EBM]] — 成本模块与世界模型可视为 EBM。
- [[02_AI/Cognitive-Architecture/Mode-1-Mode-2-Reasoning|Mode-1 / Mode-2]] — 架构中的两种决策模式。

## 来源

- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]，LeCun，2022
