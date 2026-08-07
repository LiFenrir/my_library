---
title: "Hierarchical Planning"
description: "将复杂任务分解为多个抽象层级的子目标或子任务进行分层规划"
tags: [concept, embodied-ai, robotics, planning]
created: 2026-07-30
---

# Hierarchical Planning

**核心定义**：Hierarchical Planning（分层规划）是将复杂任务分解为多个抽象层级的子目标或子任务，并在不同时间尺度上逐层求解的规划方法。

## 核心思想

- **高层规划**：决定长期目标序列（如「拿起杯子 → 倒水 → 放回杯子」）；
- **低层规划/控制**：执行具体动作（如关节轨迹、夹爪开合）。

## 形式化

常用 **Options Framework** 或 **Hierarchical Reinforcement Learning (HRL)**：

- 高层策略选择子目标或 option；
- 低层策略执行 option 直到终止条件。

## 在机器人中的应用

- 长程操作任务；
- 导航与操作组合；
- 结合 LLM/VLA 进行高层任务分解。

## 与其他概念的关系

- [[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]]|Long-Horizon Manipulatio[[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]] — 分层规划常应用于此
- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditionin[[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]] — 用子目标图像引导分层执行
- [[04_Embodied-AI/World-Model/Hierarchical-JEPA|Hierarchical JEP[[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]] — LeCun 提出的分层预测架构

## 来源

- 通用机器人规划概念
