---
title: "知识保留微调"
description: "在多任务微调时通过混合通用数据与蒸馏正则项保持模型原有通用能力。"
tags: [concept, ai, llm, fine-tuning, catastrophic-forgetting]
created: 2026-07-28
---

# 知识保留微调

核心定义：在将通用多模态模型微调到特定机器人任务时，通过数据混合与可选蒸馏正则项避免灾难性遗忘。

## 原理

- 目标函数混合多种监督：

$$
\mathcal{L} = \lambda_a \mathcal{L}_{\mathrm{act}} + \lambda_s \mathcal{L}_{\mathrm{sem}} + \lambda_g \mathcal{L}_{\mathrm{gen}} + \lambda_{kp} \mathcal{L}_{\mathrm{kp}}
$$

- $\mathcal{L}_{\mathrm{act}}$：动作任务损失；$\mathcal{L}_{\mathrm{sem}}$：领域语义损失；$\mathcal{L}_{\mathrm{gen}}$：通用字幕/VQA 损失；$\mathcal{L}_{\mathrm{kp}}$：知识保留正则项。
- 常用知识保留项：对预训练模型与当前模型输出分布的 KL 散度。

## 优缺点

- 优点：兼顾任务性能与通用能力，降低专业化后模型变窄的风险。
- 局限：需要平衡多项损失权重，通用数据比例影响收敛速度。

## 来源

- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 用于保持描述能力的同时学习空中动作与语义。
