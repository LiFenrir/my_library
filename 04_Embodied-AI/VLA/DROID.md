---
title: "DROID"
description: "大规模真实机器人操作数据集"
tags: [concept, embodied-ai, robot-learning, dataset]
created: 2026-07-31
---

# DROID

**核心定义**：DROID 是一个大规模、多样化的真实机器人操作数据集，通过多个机器人在多种场景下收集，用于训练通用的机器人操作策略与视觉-语言-动作模型。

## 关键特点

1. **规模大**：包含数十万条真实机器人操作轨迹；
2. **多样性**：覆盖多种任务、场景、机器人和相机视角；
3. **真实环境**：在真实世界采集，而非仿真；
4. **开源**：为社区提供通用预训练数据。

## 在机器人学习中的作用

- 作为 VLA 和机器人策略预训练的数据基础；
- 提供跨任务、跨环境的泛化能力；
- 常与 Open X-Embodiment 等数据集一起使用。

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — DROID 是训练 VLA 的重要数据源
- [[04_Embodied-AI/VLA/ACT|ACT]] — 可在 DROID 上训练
- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 与真实机器人数据互补

## 来源

- [[05_Papers/articles/h2r|Human-to-Robot Data Augmentation]]
