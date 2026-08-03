---
title: "Human-to-Robot Data Augmentation"
description: "将第一人称人类操作视频转换为机器人视角视频的数据增强方法"
tags: [concept, embodied-ai, data-augmentation, cross-embodiment]
created: 2026-07-29
---

# Human-to-Robot Data Augmentation (H2R)

**核心定义**：H2R 是一种数据增强方法，通过估计人类手部姿态、重定向到机器人手臂、分割并修复人手区域、合成机器人手臂图像，将第一人称人类操作视频转换为机器人视角视频。

## 动机

- 大规模机器人演示数据收集成本高
- 第一人称人类视频（Ego4D, SSv2 等）丰富但存在人与机器人之间的视觉域差距
- H2R 缩小这一差距，使人类视频更适合机器人视觉预训练

## 流程

1. 用 HaMeR 等模型估计人手 3D 姿态
2. 将动作重定向到模拟机器人手臂
3. 用 SAM 分割人手区域
4. 用 LaMa 等修复模型填充背景
5. 对齐相机内参后合成机器人手臂覆盖原图

## 优缺点

- **优点**：利用现成人类视频、提升跨 embodiment 泛化、兼容 VLA
- **缺点/局限**：重定向精度有限、合成图像可能有伪影

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — H2R 可增强 VLA 的视觉预训练
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — H2R 使用 SAM 进行手部分割
- [[04_Embodied-AI/Sim2Real/Domain-Randomization|Domain Randomization]] — 同属 sim-to-real 数据增强

## 来源

- [[05_Papers/articles/h2r|H2R: A Human-to-Robot Data Augmentation for Robot Pre-training from Videos]]
