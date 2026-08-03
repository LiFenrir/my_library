---
title: "Dynamics Model"
description: "预测系统下一状态给定当前状态与动作的模型，常用于模型-based RL、MPC 和机器人世界模型"
tags: [concept, fundamentals, ml, robotics, model-based-rl]
created: 2026-07-30
---

# Dynamics Model

**核心定义**：Dynamics Model（动力学模型）是预测环境或系统在动作作用下的状态转移的模型，形式化表示为 $p(s_{t+1} \mid s_t, a_t)$。

## 类型

- **Forward Dynamics**：预测 $s_{t+1}$ 给定 $s_t, a_t$；
- **Inverse Dynamics**：预测 $a_t$ 给定 $s_t, s_{t+1}$；
- **Latent Dynamics**：在低维隐空间中建模状态转移。

## 应用

- 模型预测控制（MPC）；
- 模型-based 强化学习；
- 机器人世界模型（预测未来观测）。

## 与其他概念的关系

- [[03_Robotics/Control/Forward-Dynamics|Forward Dynamics]] — Dynamics Model 的前向形式
- [[03_Robotics/Control/Inverse-Dynamics|Inverse Dynamics]] — Dynamics Model 的逆向形式
- [[03_Robotics/Control/Model-Predictive-Control|Model-Predictive Control]] — 使用 Forward Dynamics 做规划
- [[04_Embodied-AI/World-Model/World-Model|World Model]] — 机器人领域的 Dynamics Model 扩展

## 来源

- 通用机器人学与控制概念
