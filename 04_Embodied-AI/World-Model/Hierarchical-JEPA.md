---
title: Hierarchical JEPA
description: 在多时间尺度与多抽象层次上预测世界状态的分层联合嵌入预测架构
tags:
  - concept
  - embodied-ai
  - world-model
  - jepa
  - hierarchical-planning
  - abstraction
created: 2026-07-30
---

# Hierarchical JEPA

Hierarchical JEPA（H-JEPA）是将 [[Joint-Embedding-Predictive-Architecture|JEPA]] 堆叠成分层结构的世界模型。低层进行短程、细粒度预测；高层进行长程、抽象预测，使智能体能够在多个时间尺度和抽象层次上表示世界状态与行动计划。

## 核心思想

- 低层表示包含大量细节，适合短期预测。
- 高层表示抽象、剔除不可预测细节，适合长期预测。
- 复杂任务可逐层分解为子目标，直到最底层的毫秒级动作控制。

## 结构示例

给定观测序列 $x_0, x_1, x_2, \dots$：

- **JEPA-1**：用低层表示做短期预测。
- **JEPA-2**：以 JEPA-1 的输出为输入，提取更高层表示并做长期预测。
- 可扩展为更多层级，通过时序池化逐步粗化表示。

编码过程：

$$
s[0] = \operatorname{Enc}_1(x), \quad s_2[0] = \operatorname{Enc}_2(s[0]), \quad \dots
$$

## 分层规划

在 H-JEPA 基础上可进行 Mode-2 分层规划：

1. 高层根据高层目标 $C(s_2[4])$ 推断高层动作序列 $(a_2[2], a_2[4])$。
2. 高层“动作”并非真实动作，而是对低层状态应满足的条件。
3. 低层成本模块 $C(s[2])$、$C(s[4])$ 将这些条件转化为子目标。
4. 低层再推断低层动作序列以满足子目标。

更优做法是联合优化各层动作，而非贪婪地自顶向下。

## 不确定环境下的分层规划

每层预测器可含隐变量 $z$ 以表示不可预测因素。规划时从正则器诱导的分布中采样隐变量，生成多个可能轨迹。若每层隐变量有 $k$ 个离散取值，则 $t$ 步后轨迹数按 $k^t$ 增长，需要定向搜索与剪枝（如 MCTS）。

## 抽象概念的学习

H-JEPA 通过预测学习抽象概念：

- 预测同一物体不同视角 → 深度。
- 预测遮挡后重新出现 → 物体恒存性。
- 预测无生命物体轨迹 → 直观物理（重力、惯性）。
- 长期抽象预测 → 目标、计划、因果关系。

## 与其他概念的关系

- [[Joint-Embedding-Predictive-Architecture|JEPA]] — H-JEPA 的基础单元。
- [[World-Model]] — H-JEPA 是 LeCun 世界模型的实现形式。
- [[Model-Predictive-Control|MPC]] — H-JEPA 支持分层 MPC。
- [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|[[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]] — H-JEPA 是该架构中的世界模型核心。

## 来源

- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]，LeCun，2022
