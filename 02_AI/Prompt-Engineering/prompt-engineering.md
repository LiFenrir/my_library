---
title: "Prompt Engineering"
description: "通过设计输入提示来引导生成式模型输出期望结果的技术"
tags: [concept, ai, llm, prompt-engineering]
created: 2026-07-31
---

# Prompt Engineering

**核心定义**：Prompt Engineering（提示工程）是通过设计、优化输入给模型的提示（prompt），来引导大语言模型、视觉-语言模型或其他生成模型产生期望输出，而无需修改模型参数。

## 常见技术

- 零样本提示（Zero-shot）
- 少样本提示（Few-shot）
- 链式思考（Chain-of-Thought）
- 角色设定与系统提示
- 提示模板与变量化
- 负提示与约束提示

## 在视觉-语言模型中的应用

- 文本提示驱动开放词汇检测与分割；
- 设计任务描述引导 VLA 生成动作；
- 通过多样化提示增强数据分布覆盖。

## 与其他概念的关系

- [[02_AI/LLM/Chain-of-Thought-Reasoning|Chain-of-Thought Reasoning]] — 提示工程的一种形式
- [[02_AI/VLM/promptable-segmentation|Promptable Segmentation]] — 提示在分割任务中的具体应用
- [[02_AI/Prompt-Engineering/Prompt-Expansion|Prompt Expansion]] — 自动生成多样化提示
- [[02_AI/VLM/Grounding-DINO|Grounding DINO]] — 文本提示驱动的检测模型

## 来源

- [[05_Papers/articles/segment-anything|Segment Anything]]
