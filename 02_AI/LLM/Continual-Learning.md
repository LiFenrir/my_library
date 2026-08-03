---
title: "Continual Learning"
description: "让模型在持续接触新任务或数据时，既能学习新知识又不遗忘旧知识"
tags: [concept, ai, ml, lifelong-learning]
created: 2026-07-30
---

# Continual Learning

**核心定义**：Continual Learning（持续学习 / 终身学习）研究如何让模型在顺序学习多个任务或数据分布时，既获得新能力，又不严重遗忘已学过的知识。

## 主要策略

- **正则化方法**：限制重要参数变化（如 EWC）；
- **回放方法**：保留旧任务样本或生成伪样本；
- **架构方法**：为每个任务分配独立参数（如 Progressive Networks, Adapters）；
- **知识蒸馏**：用旧模型监督新模型。

## 挑战

- **Catastrophic Forgetting**：学习新任务后旧任务性能显著下降；
- **Forward/Backward Transfer**：新知识对旧知识的正/负迁移；
- **Task Boundary**：是否知道任务边界。

## 与其他概念的关系

- [[01_Fundamentals/ML/Catastrophic-Forgetting|Catastrophic Forgetting]] — Continual Learning 的核心敌人
- [[02_AI/LLM/Fine-Tuning|Fine-Tuning]] — 持续学习的基础操作
- [[02_AI/LLM/Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — 面向大模型的持续学习技术

## 来源

- 通用机器学习概念
