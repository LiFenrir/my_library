---
title: "RAM"
description: "自动识别图像中多个语义标签的图像标签模型"
tags: [concept, ai, computer-vision, image-tagging]
created: 2026-07-31
---

# RAM

**核心定义**：RAM（Recognize Anything Model）是一种图像标签模型，能够自动识别图像中的多个语义标签，为开放词汇检测、分割等任务提供文本输入。

## 关键能力

1. 输入图像，输出一组描述图像内容的标签；
2. 覆盖数千种常见语义概念；
3. 可作为 Grounding DINO 等开放词汇模型的自动提示生成器。

## 在 Grounded SAM 中的作用

- 自动生成图像标签，减少人工设计文本提示；
- 与 Grounding DINO 和 SAM 串联，实现从图像到标签、检测框、分割掩码的自动化流程。

## 与其他概念的关系

- [[02_AI/VLM/Grounding-DINO|Grounding DINO]] — 接收 RAM 生成的标签进行检测
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — 接收 Grounding DINO 的框进行分割
- [[02_AI/VLM/grounded-sam|Grounded SAM]] — RAM 可作为自动标注前端

## 来源

- [[05_Papers/articles/grounded-sam|Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks]]
