---
title: "VLA 动作 token 化"
description: "将机器人动作空间离散化为 token，与视觉-语言 token 在同一自回归模型中联合生成。"
tags: [concept, embodied-ai, vla, action-space, tokenization]
created: 2026-07-28
---

# VLA 动作 token 化

核心定义：把连续或离散的动作表示成语言模型词汇表中的 token，使 VLA 能统一生成文本与动作。

## 原理

- 动作被切分为短 token 序列（如 1–2 个动作 token）。
- 在推理时，动作 token 作为截止期关键路径优先解码；语义 token 则在后台低速生成。
- 支持将动作 token 映射到速度、航向、夹爪开合等外环指令。

## 优缺点

- 优点：统一自回归框架、可直接复用 LLM/VLM 解码与缓存机制。
- 局限：动作精度受离散化粒度影响，短序列表达能力有限。

## 来源

- [[05_Papers/articles/litevla-h|LiteVLA-H]]
