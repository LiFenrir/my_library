---
title: "Vision Transformer"
description: "将 Transformer 架构应用于图像块序列的计算机视觉骨干网络"
tags: [concept, ai, computer-vision, transformer]
created: 2026-07-31
---

# Vision Transformer

**核心定义**：Vision Transformer（ViT）将图像切分为固定大小的 patch，把每个 patch 当作序列 token 输入标准 Transformer 编码器，从而将 NLP 中的 Transformer 架构迁移到计算机视觉任务。

## 关键思想

1. 图像 $
abla x \in \mathbb{R}^{H \times W \times C}$ 被切分为 $N$ 个 patch；
2. 每个 patch 线性投影为向量并加入位置编码；
3. 输入 Transformer 编码器提取全局特征；
4. 在大量数据上预训练后，ViT 可达到或超过 CNN 的性能。

## 在机器人与多模态中的应用

- 作为 VLA、VLM 的视觉编码器 backbone；
- 与 CLIP 结合实现视觉-语言对齐；
- 为 SAM、DINO 等视觉基础模型提供架构基础。

## 与其他概念的关系

- [[02_AI/VLM/MAE|MAE]] — 基于 ViT 的自监督预训练方法
- [[02_AI/VLM/CLIP|CLIP]] — 使用 ViT 作为图像编码器
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — 采用 ViT 作为图像编码器
- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — ViT 是常见视觉 backbone

## 来源

- [[05_Papers/articles/segment-anything|Segment Anything]]
