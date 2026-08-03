---
title: "R3M"
description: "从人类视频中学习通用视觉表示的机器人预训练方法"
tags: [concept, embodied-ai, representation-learning, robot-learning]
created: 2026-07-31
---

# R3M

**核心定义**：R3M（Reusable Representations for Manipulation）是一种从大量人类操作视频中学习通用视觉表示的方法，旨在为机器人操作任务提供可迁移的视觉特征。

## 关键思想

1. 利用互联网上丰富的人类操作视频；
2. 通过时间对比等自监督目标学习语义与时间一致的视觉表示；
3. 预训练后的表示可用于下游机器人模仿学习与策略训练。

## 价值

- 缓解机器人视觉数据稀缺问题；
- 提供对人类操作语义敏感的视觉特征；
- 作为 VLA 或策略网络的视觉 backbone 初始化。

## 与其他概念的关系

- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 类似思路：利用人类视频辅助机器人学习
- [[01_Fundamentals/ML/Self-Supervised-Learning|Self-Supervised Learning]] — R3M 使用自监督预训练
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — R3M 表示可用于 VLA 视觉编码器

## 来源

- [[05_Papers/articles/h2r|Human-to-Robot Data Augmentation]]
