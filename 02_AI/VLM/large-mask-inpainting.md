---
title: "Large Mask Inpainting"
description: "基于快速傅里叶卷积实现大区域图像修复的方法"
tags: [concept, ai, computer-vision, inpainting]
created: 2026-07-29
---

# Large Mask Inpainting (LaMa)

**核心定义**：LaMa 是一种基于快速傅里叶卷积（Fast Fourier Convolutions, FFC）的单阶段图像修复方法，能够处理大缺失区域、复杂几何结构和高分辨率图像。

## 核心创新

1. **快速傅里叶卷积（FFC）**：提供图像全局感受野
2. **高感受野感知损失**：帮助理解全局结构
3. **大训练掩码**：释放上述组件潜力

## 优点

- 单阶段网络，结构简单
- 对大 mask 效果好
- 能泛化到比训练分辨率更高的图像
- 对周期性结构修复效果优异

## 在机器人中的应用

LaMa 等修复模型常用于 H2R 等数据增强流程中，填充被移除的人手区域。

## 与其他概念的关系

- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — LaMa 用于背景修复
- [[02_AI/VLM/promptable-segmentation|Promptable Segmentation]] — 分割与修复常配合使用

## 来源

- [[05_Papers/articles/lama|Resolution-robust Large Mask Inpainting with Fourier Convolutions]]
