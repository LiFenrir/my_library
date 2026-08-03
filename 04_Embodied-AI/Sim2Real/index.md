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

## 相关方法

- 系统辨识（System Identification）
- 域自适应（Domain Adaptation）
- 仿真到现实的渐进迁移
