---
title: "Grounding DINO"
description: "结合 DINO 检测器与 grounding 预训练的开放词汇目标检测模型"
tags: [concept, ai, computer-vision, object-detection, vlm]
created: 2026-07-31
---

# Grounding DINO

**核心定义**：Grounding DINO 是一种开放词汇目标检测模型，通过将 DINO 检测架构与语言 grounding 预训练结合，能够根据任意文本描述检测图像中的目标，无需预定义类别。

## 关键能力

1. 输入自然语言描述，输出对应的边界框；
2. 支持任意类别，不依赖训练时的固定类别集合；
3. 与 SAM 组合可形成 Grounded SAM 流程：文本 → 检测框 → 分割掩码。

## 在机器人中的应用

- 将语言指令转化为图像中的目标定位；
- 作为感知前端为 VLA / World Model 提供 mask 或边界框；
- 与 RAM/BLIP 结合实现自动文本提示生成。

## 与其他概念的关系

- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — 常与 Grounding DINO 组合
- [[02_AI/VLM/grounded-sam|Grounded SAM]] — 将 Grounding DINO 与 SAM 组装
- [[02_AI/VLM/RAM|RAM]] — 可自动生成文本标签输入 Grounding DINO
- [[02_AI/VLM/BLIP|BLIP]] — 可生成图像 caption 作为文本输入

## 来源

- [[05_Papers/articles/grounded-sam|Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks]]
