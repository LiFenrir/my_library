---
title: "Sim2Real"
description: "将仿真中训练的策略迁移到真实机器人环境的具身智能子领域"
tags: [moc, embodied-ai, sim2real]
created: 2026-07-30
---

# Sim2Real

Sim2Real 研究如何将仿真环境中训练的策略迁移到真实机器人，核心挑战是缩小仿真与现实之间的物理和视觉域差距。

## 核心概念

- [[04_Embodied-AI/Sim2Real/Domain-Randomization|Domain Randomization]] — 随机化仿真参数提升鲁棒性
- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 将人类视频转换为机器人视角数据
- [[04_Embodied-AI/Sim2Real/3d-gaussian-splatting-simulator|3D Gaussian Splatting Simulator for Robot Learning]] — 高保真可微仿真器
- [[04_Embodied-AI/Sim2Real/Train-Deploy-Alignment|Train-Deploy Alignment]] — 训练与部署对齐
- [[04_Embodied-AI/Sim2Real/Distributional-Inconsistencies-in-Robot-Learning|Distributional Inconsistencies in Robot Learning]] — 机器人学习中的分布不一致

## 相关方法

- [[04_Embodied-AI/Data-and-Evaluation/Ego-to-Robot-Synthesis|Ego-to-Robot Synthesis]] — 从人体视频合成机器人训练数据
- [[04_Embodied-AI/Data-and-Evaluation/Camera-Frame-Relative-EEF|Camera-Frame Relative EEF]] — 统一多源多形态动作表示
- 系统辨识（System Identification）
- 域自适应（Domain Adaptation）
- 仿真到现实的渐进迁移

## 相关入口

- [[04_Embodied-AI/index|04_Embodied-AI]]
- [[03_Robotics/index|03_Robotics]]
