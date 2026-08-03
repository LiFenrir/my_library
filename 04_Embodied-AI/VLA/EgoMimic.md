---
title: "EgoMimic"
description: "从第一人称人类视频中学习机器人操作策略的模仿学习方法"
tags: [concept, embodied-ai, imitation-learning, robot-learning]
created: 2026-07-31
---

# EgoMimic

**核心定义**：EgoMimic 是一类从第一人称（自我中心，egocentric）人类操作视频中学习机器人策略的模仿学习方法，利用人与机器人在观察视角上的相似性实现跨形态技能迁移。

## 关键思想

1. 采集或利用第一人称人类操作视频；
2. 学习将人类视觉观察映射到机器人动作；
3. 通过重定向、域适应或共享动作表示处理人与机器人之间的形态差异。

## 应用场景

- 厨房操作、家居整理等日常任务；
- 需要人类示范视频而非机器人示范数据的场景。

## 与其他概念的关系

- [[04_Embodied-AI/VLA/UVA|UVA]] — 同样利用人类视频
- [[04_Embodied-AI/VLA/R3M|R3M]] — 从人类视频学习视觉表示
- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 人类到机器人数据增强

## 来源

- [[05_Papers/articles/h2r|Human-to-Robot Data Augmentation]]
