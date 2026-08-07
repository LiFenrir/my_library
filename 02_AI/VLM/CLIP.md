---
title: "CLIP"
description: "通过对比学习将图像与文本映射到统一表示空间的多模态基础模型"
tags: [concept, ai, vlm, multimodal, representation-learning]
created: 2026-07-31
---

# CLIP

**核心定义**：CLIP（Contrastive Language-Image Pre-training）是 OpenAI 提出的视觉-语言基础模型，通过大规模图像-文本对的对比学习，将图像和文本映射到同一嵌入空间，从而支持零样本分类和开放词汇视觉任务。

## 关键思想

1. 使用双塔编码器分别编码图像和文本；
2. 在一个 batch 内最大化正确图像-文本对的相似度，最小化错误对的相似度；
3. 预训练后可通过文本提示完成零样本图像分类、检索等任务。

## 在机器人中的应用

- 作为 VLA 的视觉-语言对齐预训练基础；
- 提供开放词汇视觉特征用于目标检测与 grounding；
- 与 SAM 等分割模型组合实现文本驱动的分割。

## 与其他概念的关系

- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — CLIP 是典型的 VLM
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — 常与 CLIP 组合做开放词汇分割
- [[02_AI/VLM/BLIP|BLIP]] — 另一种视觉-语言预训练框架
- [[02_AI/General/Foundation-Model|Foundation Model]] — CLIP 是 CV/VLM 基础模型之一

## 来源

- [[05_Papers/articles/segment-anything|Segment Anything]]
