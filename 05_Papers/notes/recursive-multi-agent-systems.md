---
title: "RecursiveMAS: Recursive Multi-Agent Systems"
description: "递归多智能体系统，通过智能体递归分解提升复杂推理任务性能。"
tags: ["强化学习", "Multi-Agent", "LLM", "Reasoning"]
created: 2026-07-15
---

# RecursiveMAS: Recursive Multi-Agent Systems

## 基本信息
- **作者**: Xiyuan Yang, Jiaru Zou, Rui Pan, Ruizhong Qiu, Pan Lu, Shizhe Diao, Jindong Jiang, Hanghang Tong, Tong Zhang, Markus J. Buehler, Jingrui He, James Zou
- **机构**: UIUC, Stanford University, NVIDIA, MIT
- **链接**: https://recursivemas.github.io
- **发表**: 2026-04-28
- **代码**: 未公开

## 研究背景与动机

单一大语言模型在处理复杂任务时往往受限于容量不足、生成短视或解空间探索效率低等问题。多智能体系统（MAS）通过让多个专业智能体协作来扩展性能，但现有方法存在两个瓶颈：

1. **文本交互延迟高**：智能体必须等待其他智能体完成生成才能继续，顺序依赖引入大量延迟
2. **训练困难**：更新所有模型参数非平凡，且文本交互中的顺序依赖使梯度传播复杂

本文提出将递归语言模型（RLM）的缩放原则从单模型扩展到多智能体系统，将整个系统视为统一的潜在空间递归计算。

![[99_Attachments/papers/images/recursive-multi-agent-systems/5035fec9064e0ec1c77c6cb81074a8d2563e28a0e5ad1b75fb9912ffbc2183b0.jpg]]

## 核心方法: RecursiveMAS

### RecursiveLink 模块
轻量级的两层残差投影模块，用于潜在状态传输和精炼：

- **Inner RecursiveLink**：在每个智能体内部，整合输入和输出空间之间的持续潜在思考
- **Outer RecursiveLink**：桥接不同模型类型和规模的异构智能体的隐藏表示，实现无缝跨智能体交互

### 内外循环训练范式

**内循环**：训练每个智能体的 Inner RecursiveLink，使其更好地对齐潜在思考生成，提供模型级预热

**外循环**：在系统级训练跨智能体的 Outer RecursiveLink，梯度通过递归轮次的完整计算迹递归反向传播

### 理论分析

1. **运行时复杂度**：RecursiveLink 实现潜在空间信息的直接转换，避免重复解码中间智能体，比文本交互更高效
2. **学习动态**：潜在空间连接在训练期间保持跨递归轮次的稳定梯度传播流，避免文本交互引起的梯度消失

## 实验结果

**评估基准**：9 个基准，涵盖数学、科学、医学、搜索和代码生成

**智能体配置**：Qwen3/3.5, LLama-3, Gemma3, Mistral（sub-1.5B 到 5-10B）

**协作模式**：
- Sequential：逐步顺序推理
- Mixture-of-Experts：专家混合协作
- Distillation：专家到学习者的知识蒸馏
- Deliberation：工具集成审议

**主要结果**：
- 平均准确率提升 **8.3%**
- 端到端推理加速 **1.2×–2.4×**
- Token 使用量减少 **34.6%–75.6%**

![[99_Attachments/papers/images/recursive-multi-agent-systems/a4750c6246e1871eb85f47793393a5b5c2fb97153c5ef1e877b57a54a9467b12.jpg]]

## 核心贡献

1. **RecursiveMAS 框架**：将多智能体协作重新定义为潜在空间递归计算
2. **RecursiveLink 模块**：轻量级连接异构智能体，实现分布内潜在思考生成和跨智能体状态传输
3. **内外循环训练**：通过共享梯度信用分配进行迭代全系统协同优化
4. **结构无关性**：可泛化到多种协作模式，无需固定架构

## 个人思考

- **创新点**：将单模型递归扩展到系统级递归是自然的下一步，潜在空间交互避免了文本生成的瓶颈
- **实用性**：轻量级 RecursiveLink 使大规模异构智能体协作成为可能，对实际部署友好
- **局限**：仅在文本推理任务上验证，未涉及具身智能或视觉任务；智能体数量扩展性待验证
- **扩展方向**：结合 VLA 模型进行多模态递归协作；探索动态智能体组合策略


## 原文

[[05_Papers/articles/recursive-multi-agent-systems|recursive-multi-agent-systems]]
