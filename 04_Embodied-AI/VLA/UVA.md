---
title: "UVA"
description: "利用无约束人类视频学习机器人视觉-动作策略的方法"
tags: [concept, embodied-ai, imitation-learning, robot-learning]
created: 2026-07-31
---

# UVA

**核心定义**：UVA（Unconstrained Video-to-Action）是一类利用无约束、野外人类视频学习机器人动作策略的方法，旨在从互联网规模的人类活动视频中提取可供机器人执行的技能。

## 关键思想

1. 利用大量无约束人类视频（如 YouTube、Ego4D）；
2. 学习目标跟踪、手-物交互、动作阶段等中间表示；
3. 将人类动作语义重定向到机器人动作空间。

## 挑战

- 人类视频缺乏机器人动作标注；
- 人与机器人形态差异大；
- 需要处理遮挡、视角变化与背景复杂场景。

## 与其他概念的关系

- [[04_Embodied-AI/VLA/EgoMimic|EgoMimic]] — 同样从第一人称人类视频学习
- [[04_Embodied-AI/VLA/R3M|R3M]] — 从人类视频学习视觉表示
- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 人类到机器人数据迁移

## 来源

- [[05_Papers/articles/h2r|Human-to-Robot Data Augmentation]]
