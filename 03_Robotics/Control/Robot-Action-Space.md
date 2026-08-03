---
title: Robot Action Space
description: 机器人策略输出动作的常见表示形式，包括关节空间与末端执行器空间控制
tags:
  - robotics
  - control
  - action-space
  - robot-learning
created: 2026-07-28
---

# Robot Action Space

Robot Action Space 定义了机器人策略输出的**控制信号形式**，常见的有关节空间（joint-space）和末端执行器空间（end-effector space）两种。

## Joint-Space Control

输出机器人各关节的目标位置或速度。

- **优点**：直接对应机器人底层执行器，避免逆运动学数值误差
- **缺点**：不同机器人关节结构不同，跨 embodiment 迁移时需要额外适配

## End-Effector Control

输出末端执行器在笛卡尔空间中的目标位姿（位置 + 姿态）。

- **优点**：与具体机器人形态解耦，便于跨 embodiment 泛化
- **缺点**：需要通过逆运动学（IK）转换为关节目标，引入额外计算和误差

## Hybrid Training

一些 VLA 在训练时同时包含两种控制模式，并通过文本标识符让模型知道当前使用哪种模式，测试时可根据任务选择。

## Related Concepts

- [[03_Robotics/Control/Robot-Observation-Space|Robot Observation Space]] — 策略输入的状态表示
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 输出机器人动作的策略
- [[04_Embodied-AI/VLA/Cross-embodiment-Generalization|Cross-embodiment Generalization]] — 动作空间选择影响跨形态迁移

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 同时训练 joint 和 end-effector 两种控制模式
