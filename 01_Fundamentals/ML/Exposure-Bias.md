---
title: "Exposure Bias"
description: "序列生成模型在训练时使用真实历史而在测试时使用生成历史导致的分布不一致问题"
tags: [concept, fundamentals, ml, sequence-modeling]
created: 2026-07-30
---

# Exposure Bias

**核心定义**：Exposure Bias 指序列生成模型在训练时依赖真实历史 token（Teacher Forcing），而在测试/推理时必须依赖自身生成的历史，导致训练分布与测试分布不一致的问题。

## 影响

- 模型在训练时未见过自身错误，无法学习错误恢复；
- 测试时小错误会随序列长度累积，导致生成质量下降。

## 缓解方法

- **Scheduled Sampling**：以一定概率用模型自身输出替代真实 token；
- **Data Noising**：向输入加入噪声提高鲁棒性；
- **SeqGAN / RL 训练**：直接优化测试时生成指标；
- **Professor Forcing**：匹配训练与测试时的隐状态分布。

## 与其他概念的关系

- [[01_Fundamentals/ML/Teacher-Forcing|Teacher Forcing]] — Exposure Bias 的主要来源
- [[01_Fundamentals/ML/Scheduled-Sampling|Scheduled Sampling]] — 常用缓解方法
- [[01_Fundamentals/ML/Autoregressive-Model|Autoregressive Model]] — 常出现 Exposure Bias 的模型

## 来源

- 通用序列建模概念
