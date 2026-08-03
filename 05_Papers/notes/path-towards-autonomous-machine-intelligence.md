---
title: "A Path Towards Autonomous Machine Intelligence"
description: "Yann LeCun 提出的自主机器智能路径，强调基于 JEPA 的世界模型与自监督学习。"
tags: ["世界模型", "自监督学习", "认知架构", "JEPA", "能量模型", "内在动机"]
created: 2026-07-15
---

# A Path Towards Autonomous Machine Intelligence

## 基本信息
- **作者**: Yann LeCun (NYU Courant Institute / Meta FAIR)
- **链接**: [arXiv:2210.08352](https://arxiv.org/abs/2210.08352) (后续正式版本)
- **版本**: v0.9.2, 2022-06-27
- **类型**: 立场论文 (Position Paper)
- **本地路径**: `../articles/path-towards-autonomous-machine-intelligence.md`

## 研究背景与动机

当前 AI/ML 系统远不及人类和动物的学习能力：
- 青少年仅需约 20 小时练习就能学会开车
- 儿童通过少量接触就能学会语言
- 人类能在从未遇到的情况下知道如何行动

相比之下，当前 ML 系统需要海量训练数据、数百万 RL 试验，工程师还要硬编码数百种行为，仍无法在真实任务中达到人类可靠性。

**核心假设**: 答案在于人类和动物学习**世界模型**（world models）的能力——内部的世界运作模型。

## 三大挑战

1. **表示学习**: 机器如何通过观察学习世界表示、预测和行动？
   - 真实世界交互昂贵且危险，智能体应尽可能通过观察学习

2. **推理与规划**: 如何与基于梯度的学习兼容？
   - 最佳学习方法依赖梯度估计，难以与基于逻辑的符号推理调和

3. **层次化抽象**: 多时间尺度、多抽象层次的表示
   - 人类能将复杂动作分解为低级动作序列，进行长期预测和规划

## 核心架构

![[99_Attachments/papers/images/path-towards-autonomous-machine-intelligence/lecue_architecture.jpg]]
*图2: 自主智能体系统架构。所有模块都是可微分的。*

### 模块组成

| 模块 | 功能 |
|------|------|
| **Configurator** | 执行控制，配置其他模块执行当前任务 |
| **Perception** | 接收传感器信号，估计当前世界状态 |
| **World Model** | 估计缺失信息，预测未来世界状态 |
| **Cost Module** | 计算"能量"衡量智能体不适程度 |
| **Short-term Memory** | 存储过去、当前和预测的世界状态 |
| **Actor** | 计算动作序列提案，输出动作到执行器 |

### Cost Module 细节

![[99_Attachments/papers/images/path-towards-autonomous-machine-intelligence/lecue_cost_module.jpg]]
*图6: Cost Module 架构。包含不可变的 Intrinsic Cost 和可训练的 Critic。*

$$
C(s) = IC(s) + TC(s)
$$

- **Intrinsic Cost (IC)**: 硬编码，不可训练。定义智能体的基本行为本质（疼痛、愉悦、饥饿、好奇心等）
- **Trainable Critic (TC)**: 可训练，预测未来内在能量，让 configurator 专注于子目标

## 两种运行模式

### Mode-1: 反应式行为 (System 1)

![[99_Attachments/papers/images/path-towards-autonomous-machine-intelligence/lecue_mode2.jpg]]
*图3: Mode-1 感知-动作循环。*

- 感知模块提取世界状态表示 $s[0] = Enc(x)$
- 策略模块直接产生动作 $a[0] = A(s[0])$
- 不涉及世界模型的复杂推理
- 类似 Kahneman 的"系统1"

### Mode-2: 推理与规划 (System 2)

![[99_Attachments/papers/images/path-towards-autonomous-machine-intelligence/lecue_mode2.jpg]]
*图4: Mode-2 感知-动作循环。通过世界模型模拟和优化。*

1. **感知**: 提取当前状态 $s[0] = P(x)$
2. **动作提案**: Actor 提出动作序列 $(a[0], ..., a[T])$
3. **模拟**: 世界模型预测状态序列 $(s[1], ..., s[T])$
4. **评估**: Cost 计算总成本 $F(x) = \sum_{t=1}^{T} C(s[t])$
5. **规划**: 通过梯度优化找到低成本动作序列
6. **执行**: 输出最优序列的第一个动作
7. **记忆**: 存储状态和成本用于后续训练

本质上是**模型预测控制 (MPC)**，但世界模型和成本函数是学习得到的。

### Mode-2 → Mode-1: 技能学习

![[99_Attachments/papers/images/path-towards-autonomous-machine-intelligence/lecue_mode2_training.jpg]]
*图5: 用 Mode-2 结果训练反应式策略模块。*

- Mode-2 计算量大，一次只能处理一个复杂任务
- 用 Mode-2 产生最优动作序列，训练策略模块 $A(s[t])$ 近似最优动作
- 训练后的策略可在 Mode-1 中直接使用，实现"编译"新技能

## 世界模型的设计与训练

### 自监督学习 (SSL) 框架

核心思想：**模式补全** (pattern completion)

- 不强制模型从 $x$ 预测 $y$（因为可能有无限多个兼容的 $y$）
- 而是训练系统判断 $x$ 和 $y$ 是否兼容
- 使用**能量模型 (EBM)**：$F(x, y)$ 在兼容时输出低能量

### JEPA: Joint Embedding Predictive Architecture

**核心原则**: 给定 $x$ 和 $y$，学习两个编码器：
- $s_x = g_x(x)$，$s_y = g_y(y)$
- (1) $s_x$ 和 $s_y$ 对 $x$ 和 $y$ 信息最大化
- (2) $s_y$ 可轻易从 $s_x$ 预测

**非生成式**: 不预测原始输入，而是在表示空间中预测

### 层次化 JEPA (H-JEPA)

![[99_Attachments/papers/images/path-towards-autonomous-machine-intelligence/lecue_infant.jpg]]
*图1: 婴儿概念习得时间线。抽象概念建立在低级概念之上。*

- 低级：边缘、轮廓、深度图
- 中级：物体、遮挡、刚性运动
- 高级：直觉物理（稳定性、重力、惯性）
- 更高级：因果关系、语言、社会知识

## 关键创新点

1. **可配置世界模型**: 单一世界模型引擎，动态配置用于不同任务
2. **JEPA 架构**: 非生成式预测，在表示空间操作
3. **非对比自监督学习**: 无需负样本，同时保证信息性和可预测性
4. **层次化规划**: 多时间尺度、多抽象层次的推理
5. **能量最小化推理**: 将推理视为约束满足/能量最小化

## 与当前研究的关联

- **世界模型**: 与 Ha & Schmidhuber (2018) 的世界模型、Dreamer 系列相关
- **自监督学习**: 延续 LeCun 长期倡导的 SSL 路线
- **模型预测控制**: 与机器人学中的 MPC 传统相连
- **能量模型**: 基于 LeCun 早期的 EBM 工作

## 个人评价

**意义**: 这是 LeCun 对 AGI 路径最系统的阐述，将深度学习、认知科学和控制论统一在一个框架下。

**影响**: 
- I-JEPA 和 V-JEPA 是此框架的具体实现
- 对当前世界模型研究（如 Sora、GPT-4o）有深远影响

**局限**:
- 立场论文，缺乏具体实验验证
- 世界模型的训练细节（特别是多模态预测）仍具挑战性
- 内在成本模块的设计需要大量领域知识

## 相关论文

- [[world-models]] - Ha & Schmidhuber 的原始世界模型
- [[privileged-foresight-distillation]] - 世界模型蒸馏方法
- [[rise]] - 基于组合世界模型的自改进策略


## 原文

[[05_Papers/articles/path-towards-autonomous-machine-intelligence|path-towards-autonomous-machine-intelligence]]
