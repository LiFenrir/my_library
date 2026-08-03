---
title: Vision-Language Model
description: 同时处理视觉与语言输入并输出文本或嵌入的多模态基础模型
tags:
  - ai
  - multimodal
  - vlm
  - foundation-model
created: 2026-07-28
---

# Vision-Language Model

Vision-Language Model（VLM）是一类能够**联合理解图像与文本**并生成文本响应的多模态基础模型。

## Core Idea

将视觉编码器（如 ViT）与大语言模型（LLM）结合，使模型能够基于图像内容进行推理、描述、问答和指令遵循。

## Typical Architecture

- **Vision Encoder**：将图像编码为视觉 token
- **Projector / Adapter**：对齐视觉与语言表示空间
- **Language Model Backbone**：处理多模态 token 并生成输出

## Key Capabilities

- 图像描述与视觉问答
- 视觉指令遵循
- 零样本视觉理解
- 多模态上下文学习

## In Robotics

VLM 常被用作 Vision-Language-Action（VLA）模型的感知与语言理解 backbone，提供场景语义和指令解析能力。

## Related Concepts

- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 在 VLM 基础上增加动作输出的机器人策略
- [[04_Embodied-AI/VLA/Action-Expert|Action Expert]] — VLA 中负责生成动作的专业模块
- [[04_Embodied-AI/VLA/Knowledge-Insulation|Knowledge Insulation]] — 保护 VLM backbone 表示不被动作梯度破坏的训练技巧

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 使用 Gemma3 4B VLM 作为 backbone
