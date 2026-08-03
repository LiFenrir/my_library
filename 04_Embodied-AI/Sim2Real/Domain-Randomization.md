---
title: "Domain Randomization"
description: "在仿真中随机化环境参数以训练对真实世界变化更鲁棒的策略"
tags: [concept, embodied-ai, sim2real, domain-randomization]
created: 2026-07-30
---

# Domain Randomization

**核心定义**：Domain Randomization 是一种 Sim2Real 技术，通过在训练时随机化仿真环境的物理参数、视觉外观、动力学等，使策略学习到对域差异鲁棒的特征，从而迁移到真实世界。

## 随机化维度

- 物理参数：摩擦、质量、阻尼、关节限制；
- 视觉外观：纹理、光照、背景、相机参数；
- 动力学：动作延迟、观测噪声、执行器误差。

## 核心假设

如果训练时覆盖了足够宽的参数分布，真实世界可被视为该分布内的一个样本，策略就能泛化。

## 优缺点

- **优点**：无需真实世界数据即可提升 Sim2Real 迁移；
- **缺点**：过度随机化会增加学习难度；分布设计需要领域知识。

## 与其他概念的关系

- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 同属 Sim2Real 数据增强
- [[04_Embodied-AI/Sim2Real/3d-gaussian-splatting-simulator|3D Gaussian Splatting Simulator]] — 可结合 Domain Randomization 生成多样化视觉数据

## 来源

- Tobin et al., 2017, "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
