---
title: Aleatoric vs Epistemic Uncertainty
description: 机器学习与预测模型中两类不确定性的区分：数据内在随机性与知识不足
tags:
  - concept
  - ml
  - uncertainty
  - probabilistic-modeling
  - world-model
  - bayesian-deep-learning
created: 2026-07-30
---

# Aleatoric vs Epistemic Uncertainty

在预测模型（尤其是世界模型）中，不确定性可分为两类：Aleatoric Uncertainty（偶然不确定性）和 Epistemic Uncertainty（认知不确定性）。区分二者对规划、探索和安全决策至关重要。

## Aleatoric Uncertainty（偶然不确定性）

来源：世界本身的随机性或不可约简的混沌。

- 环境内在随机性（如掷骰子、交通中其他车辆的决策）。
- 确定性但混沌的系统（如天气、多体碰撞），需要无限精确感知才能预测。
- 确定性但部分可观测的系统（智能体无法看到完整状态）。

**特点**：

- 无法通过收集更多数据消除。
- 通常用隐变量、概率分布或混合模型表示。
- 在 LeCun 的架构中，由预测器的隐变量 $z$ 捕获。

## Epistemic Uncertainty（认知不确定性）

来源：模型或感知对真实状态的知识不足。

- 传感器只提供部分信息（如遮挡、有限视野）。
- 感知模块提取的表示不包含预测所需的全部信息。
- 模型表达能力有限（bounded rationality）。
- 训练数据不足，模型未见过某些状态分布。

**特点**：

- 可通过更多数据、更好模型或更完整感知降低。
- 在规划中应驱动探索：智能体应主动收集能减少认知不确定性的信息。

## 在世界模型中的表示

LeCun 的隐变量 EBM 框架将所有不确定性统一压缩到隐变量 $z$ 中：

- $z$ 表示当前世界状态或动作后果中无法从已知信息推断的部分。
- 规划时从 $z$ 的分布中采样，生成多个可能轨迹。
- 对离散 $z$，$t$ 步后轨迹数按 $k^t$ 增长，需要搜索与剪枝。

## 对规划的影响

- 仅优化期望成本可能导致风险敏感行为。
- 可同时考虑成本均值与方差，选择鲁棒动作。
- 高认知不确定区域应成为主动探索目标（好奇心驱动）。

## 与其他概念的关系

- [[Energy-Based-Model|EBM]] — 用隐变量和能量函数统一表示不确定性。
- [[Joint-Embedding-Predictive-Architecture|JEPA]] — 通过隐变量 $z$ 处理不可预测的未来。
- [[Hierarchical-JEPA|H-JEPA]] — 在多层抽象上同时处理不确定性。
- [[Model-Predictive-Control|MPC]] — 不确定环境下的规划基础。

## 来源

- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]，LeCun，2022
