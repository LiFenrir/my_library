---
title: "BLIP"
description: "统一理解与生成任务的视觉-语言预训练框架"
tags: [concept, ai, vlm, multimodal, captioning]
created: 2026-07-31
---

# BLIP

**核心定义**：BLIP（Bootstrapping Language-Image Pre-training）是一个统一的视觉-语言预训练框架，通过多任务目标（图像-文本对比、图像-文本匹配、图像 caption 生成）和噪声数据过滤，提升视觉-语言理解与生成能力。

## 关键能力

1. 图像-文本检索；
2. 图像 caption 生成；
3. 视觉问答（VQA）；
4. 可作为自动标注前端生成文本描述。

## 在机器人中的应用

- 为 Grounded SAM 等流程提供图像 caption 或文本提示；
- 用于机器人场景语义描述与数据标注。

## 与其他概念的关系

- [[02_AI/VLM/CLIP|CLIP]] — 另一种视觉-语言预训练方法
- [[02_AI/VLM/grounded-sam|Grounded SAM]] — BLIP 可作为自动标注前端
- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — BLIP 是典型的 VLM

## 来源

- [[05_Papers/articles/grounded-sam|Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks]]
