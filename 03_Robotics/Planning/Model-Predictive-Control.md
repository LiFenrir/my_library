---
title: Model-Predictive Control
description: 利用前向模型预测未来状态并在滚动时域内优化动作序列的控制方法
tags:
  - concept
  - robotics
  - control
  - planning
  - model-based-rl
  - world-model
created: 2026-07-30
---

# Model-Predictive Control

Model-Predictive Control（MPC）是一类基于前向模型的控制方法：在每一步利用系统动力学模型预测未来状态序列，并优化一段有限时域内的动作序列，然后只执行第一个动作，再重新规划。

## 核心流程

1. 估计当前状态 $s[0]$。
2. 提出动作序列 $(a[0], \dots, a[T])$。
3. 用前向模型预测未来状态：

$$
s[t+1] = \operatorname{Pred}(s[t], a[t])
$$

4. 计算累计成本：

$$
F = \sum_{t=1}^{T} C(s[t])
$$

5. 优化动作序列以最小化 $F$。
6. 执行第一个动作（或前几个动作），滚动重复。

## 与可学习世界模型的结合

传统 MPC 假设动力学模型已知。在 LeCun 的架构中，World Model 从数据中学习得到，因此 MPC 成为世界模型驱动的 Mode-2 规划方式。由于世界模型和成本模块可微，可用梯度法优化动作序列。

## 优化方法

- **梯度法**：当模型与成本光滑时，通过反向传播梯度到动作变量。
- **动态规划**：动作空间离散且较小时适用。
- **梯度-free 方法**：MCTS、模拟退火、启发式搜索、组合优化等，用于不光滑或离散动作空间。

## 不确定性处理

真实环境存在多种不确定性：

- 内在随机性（aleatoric）。
- 部分可观测（epistemic）。
- 模型不完美。

可通过隐变量表示未观测因素，在规划时采样多个轨迹，再优化平均成本或风险调整成本。

## 与其他概念的关系

- [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|[[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]] — Mode-2 规划即 MPC 的学习版本。
- [[02_AI/Cognitive-Architecture/Mode-1-Mode-2-Reasoning|Mode-1 / Mode-2]] — Mode-2 对应 MPC。
- [[World-Model]] — MPC 的前向模型。
- [[Hierarchical-JEPA|H-JEPA]] — 支持分层 MPC。

## 来源

- Bryson & Ho, 1969
- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]，LeCun，2022
