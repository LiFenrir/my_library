---
title: "RoVi-Aug"
description: "面向机器人视觉的鲁棒数据增强方法"
tags: [concept, embodied-ai, robot-learning, data-augmentation]
created: 2026-07-31
---

# RoVi-Aug

**核心定义**：RoVi-Aug（Robotic Visual Augmentation）是面向机器人学习场景的视觉数据增强方法，通过对机器人操作视频或图像进行变换，提升策略对视觉变化的泛化能力。

## 关键思想

- 对视觉输入施加颜色抖动、裁剪、遮挡、风格化等增强；
- 在训练时增加视觉分布多样性；
- 提高策略在不同光照、背景、物体外观下的鲁棒性。

## 与 H2R 的关系

H2R 和 RoVi-Aug 都关注通过数据增强提升机器人学习，但 H2R 侧重于将人类视频转换为机器人训练数据，而 RoVi-Aug 侧重于对已有视觉数据进行增强。

## 与其他概念的关系

- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 人类视频到机器人数据的增强
- [[04_Embodied-AI/Sim2Real/Domain-Randomization|Domain Randomization]] — 通过仿真域随机化提升泛化
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 数据增强可提升 VLA 视觉泛化

## 来源

- [[05_Papers/articles/h2r|Human-to-Robot Data Augmentation]]
