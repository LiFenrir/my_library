---
title: "MAE"
description: "通过高比例掩码图像块自编码学习视觉表示的自监督方法"
tags: [concept, ai, computer-vision, self-supervised-learning]
created: 2026-07-31
---

# MAE

**核心定义**：MAE（Masked Autoencoder）是视觉领域的自监督预训练方法，通过随机高比例掩码输入图像块，让模型基于可见块重建被掩码的像素或特征，从而学习有用的视觉表示。

## 关键思想

1. 将图像切分为 patch；
2. 随机掩码大部分 patch（如 75%）；
3. 用非对称编码器-解码器结构重建掩码区域；
4. 预训练后的编码器可作为下游任务的视觉 backbone。

## 与机器人学习的关联

MAE 预训练得到的视觉 backbone 常被用于机器人策略、VLA 和模仿学习，提供对场景几何与物体外观的通用理解。

## 与其他概念的关系

- [[02_AI/VLM/Vision-Transformer|Vision Transformer]] — MAE 基于 ViT 架构
- [[01_Fundamentals/ML/Self-Supervised-Learning|Self-Supervised Learning]] — MAE 是自监督表示学习的一种
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — SAM 的视觉 backbone 也使用了 MAE 风格预训练

## 来源

- [[05_Papers/articles/segment-anything|Segment Anything]]
- [[05_Papers/articles/h2r|Human-to-Robot Data Augmentation]]
