---
title: "Cross-Modal Attention"
description: "在不同模态（如视觉、语言、动作）表示之间计算注意力以实现多模态对齐与融合的机制"
tags: [concept, ai, multimodal, attention]
created: 2026-07-30
---

# Cross-Modal Attention

**核心定义**：Cross-Modal Attention 是一种注意力机制，允许一个模态的查询（query）去关注另一个模态的键-值（key-value），从而实现不同模态之间的信息对齐与融合。

## 形式化

给定模态 A 的查询 $Q_A$ 和模态 B 的键值 $K_B, V_B$：

$$
\text{Attention}(Q_A, K_B, V_B) = \text{softmax}\left(\frac{Q_A K_B^T}{\sqrt{d_k}}\right) V_B
$$

## 应用

- 视觉-语言模型（VLM）中的图像-文本对齐；
- 视觉-语言-动作模型（VLA）中动作专家对视觉-语言上下文的关注；
- 多模态 Transformer（如 ViLBERT, LXMERT）。

## 与 Self-Attention 的区别

- **Self-Attention**：$Q, K, V$ 来自同一模态；
- **Cross-Modal Attention**：$Q$ 来自一个模态，$K, V$ 来自另一个模态。

## 与其他概念的关系

- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — Cross-Modal Attention 的主要应用
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 三模态融合
- [[02_AI/LLM/Mixture-of-Transformers|Mixture of Transformers]] — 可用 Cross-Modal Attention 实现模态间信息交换

## 来源

- 通用多模态学习概念
