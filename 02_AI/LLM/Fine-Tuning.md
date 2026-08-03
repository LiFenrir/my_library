---
title: "Fine-Tuning"
description: "在预训练模型基础上，用特定任务数据继续训练以适应下游任务"
tags: [concept, ai, llm, transfer-learning]
created: 2026-07-30
---

# Fine-Tuning

**核心定义**：Fine-Tuning（微调）是在大规模预训练模型基础上，使用下游任务数据继续训练模型参数，使模型适应特定任务的过程。

## 常见方式

- **Full Fine-Tuning**：更新所有参数；
- **LoRA / QLoRA**：只训练低秩适配器，保持 backbone 冻结；
- **Prompt Tuning**：优化输入提示嵌入；
- **Adapter Tuning**：在模型层间插入小型适配器。

## 挑战

- **Catastrophic Forgetting**：微调后丢失预训练知识；
- **Overfitting**：下游数据量少时容易过拟合；
- **Compute Cost**：大模型全量微调计算昂贵。

## 与其他概念的关系

- [[02_AI/LLM/Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — 缓解灾难性遗忘的微调方法
- [[02_AI/LLM/Continual-Learning|Continual Learning]] — 多任务连续微调场景
- [[01_Fundamentals/ML/Catastrophic-Forgetting|Catastrophic Forgetting]] — 微调常见问题

## 来源

- 通用深度学习概念
