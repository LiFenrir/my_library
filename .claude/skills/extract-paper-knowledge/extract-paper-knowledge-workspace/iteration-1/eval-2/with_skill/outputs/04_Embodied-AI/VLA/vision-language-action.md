---
title: "Vision-Language-Action (VLA) Model"
description: "将视觉感知、自然语言指令与机器人动作统一在单个自回归模型中的策略表示。"
tags: [concept, embodied-ai, vla, multimodal]
created: 2026-07-28
---

# Vision-Language-Action (VLA) Model

核心定义：把视觉观测、语言任务描述与机器人动作映射放在同一个模型里，让策略同时具备语义理解与动作生成能力。

## 原理

- 以[[vision-language-model|视觉-语言模型（VLM）]]或[[large-language-model|大语言模型（LLM）]]为骨干。
- 机器人动作被离散化为 token，与文本 token 在同一自回归框架中联合预测。
- 典型流程：视觉编码 → 投影/提示打包 → 自回归解码 → 输出动作 token 或语义 token。

## 与其他概念的关系

- [[vision-language-model|VLM]] — VLA 通常继承 VLM 的预训练权重与多模态表示。
- [[action-tokenization|动作 token 化]] — 动作空间离散化是 VLA 的关键实现前提。
- [[dual-rate-vla-scheduler|双速率 VLA 调度]] — 同一 VLA 同时服务高频动作与低频语义。

## 优缺点

- 优点：语义泛化强、任务描述自然、可利用互联网预训练知识。
- 局限：推理延迟高、对计算资源敏感、动作精度受 token 粒度限制。

## 来源

- [[05_Papers/articles/litevla-h|LiteVLA-H: Dual-Rate Vision-Language-Action Inference for Onboard Aerial Guidance and Semantic Perception]]
- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]
