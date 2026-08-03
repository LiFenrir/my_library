---
title: "Grounded SAM"
description: "将开放词汇检测（Grounding DINO）与通用分割（SAM）组装，实现文本驱动的开放世界图像分割"
tags: [concept, ai, computer-vision, segmentation, open-vocabulary]
created: 2026-07-30
---

# Grounded SAM

**核心定义**：Grounded SAM 是一种将开放词汇目标检测器 Grounding DINO 与通用分割模型 SAM 组装起来的视觉系统，能够通过任意自由形式文本提示直接输出对应对象的精确分割掩码。

## 为什么需要

单独模型各有短板：

- **SAM**：能分割任意物体，但需要点、框等空间提示，无法直接理解文本类别；
- **Grounding DINO**：能根据文本检测任意类别，但只输出边界框。

组合两者可实现「说出一个词，分割对应物体」的开放世界文本驱动分割。

## 架构

1. **文本提示** → Grounding DINO 生成带类别的边界框；
2. **边界框** → 作为 SAM 的提示输入；
3. **SAM** → 输出精细分割掩码。

整个流程无需重新训练 SAM 或 Grounding DINO，通过组合已有专家模型实现新能力。

## 优缺点

- **优点**：
  - 零样本开放词汇分割；
  - 利用两个预训练基础模型，无需额外大规模训练；
  - 可扩展至多任务视觉管线（检测、分割、Captioning 等）。
- **缺点/局限**：
  - 错误会在模块间级联传播；
  - 检测器失败直接导致分割失败；
  - 对复杂语义关系（如「穿红衣服的人」）仍可能出错。

## 与其他概念的关系

- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — 提供通用分割能力
- [[02_AI/VLM/promptable-segmentation|Promptable Segmentation]] — Grounded SAM 是该范式的文本提示实现
- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — 文本理解与视觉 grounding 的基础

## 来源

- [[05_Papers/articles/grounded-sam|Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks]]
