---
title: Foundation Model
description: 在大规模广泛数据上训练、可通过提示或微调适配多种下游任务的通用模型范式
tags:
  - concept
  - ai
  - foundation-model
  - transfer-learning
  - prompt-engineering
created: 2026-07-30
---

# Foundation Model

**核心定义**：Foundation model 指在广泛数据上大规模预训练、并可通过提示工程（prompt engineering）或微调适配到多种下游任务的模型。

## 关键特征

1. **大规模预训练**：在海量、多样化的数据上训练，通常远超单一任务数据集。
2. **通用能力**：不是为某个固定任务设计，而是具备迁移到新任务、新分布的潜力。
3. **可组合性**：可作为更大系统中的组件，通过接口与其他模块组合产生新能力。
4. **提示驱动**：下游任务常通过设计合适的提示（文本、点、框、图像等）直接调用，无需重新训练。

## 主要领域

| 领域 | 代表工作 | 提示形式 |
|------|----------|----------|
| 自然语言处理 | GPT、PaLM | 文本 |
| 视觉-语言 | CLIP、ALIGN | 文本/图像 |
| 图像分割 | SAM | 点、框、掩码、文本 |
| 机器人 | π0、RT-2 | 视觉-语言指令 |

## 训练范式的两个分支

1. **自监督预训练主导**：强调通过自监督目标（如语言建模、掩码重建）获得通用表示。
2. **数据引擎 + 有监督训练**：当可通过模型辅助标注扩展高质量标签时，有监督训练同样能构建强基础模型。

## 与 Prompt Engineering 的关系

Foundation model 的零样本/少样本能力通常通过提示工程实现。提示将下游任务重新表述为模型预训练时熟悉的形式，从而避免为每个任务单独训练。

## 局限性

- 通常只在训练数据的分布内表现可靠，跨域迁移仍有风险。
- 可能继承训练数据中的偏见。
- 作为通用组件时，接口设计（如“有效输出”的定义）决定了组合系统的可靠性。

## 与其他概念的关系

- [[02_AI/VLM/promptable-segmentation|Promptable Segmentation]] — 分割领域的基础模型任务范式
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — 分割基础模型的代表实现
- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — 视觉-语言基础模型

## 来源

- [[05_Papers/articles/segment-anything|Segment Anything]]，第 8 节 Discussion
- Bommasani et al., "On the Opportunities and Risks of Foundation Models" (2021)
