---
title: "Flow Matching 生成建模"
description: "从概率密度路径与向量场角度理解 flow matching，及其在条件连续多峰动作生成中的应用。"
tags: [fundamentals, ml, generative-model, flow-matching]
created: 2026-07-28
---

# Flow Matching 生成建模

Flow matching 通过拟合一个向量场，将简单基分布沿着连续概率密度路径变换到目标分布，无需显式建模似然。

- **条件流匹配（CFM）**：给定上下文条件 $c$ 学习条件向量场，使生成过程可控；适用于图像、动作等连续输出。
- **动作生成视角**：在机器人策略中，动作空间通常是连续且多峰的；flow matching 目标（或扩散目标）能自然刻画“同一状态下多种可行动作”的分布。
- **与 VLA 的关系**：VLA 中的 action expert 常以 flow matching 为目标，预测一段连续动作块（action chunk）。这不是机器人专属技巧，而是通用生成模型方法在动作生成上的应用。
- **Classifier-Free Guidance**：训练时随机 dropout 条件，推理时用正负条件分数差进行引导，可强化对指定上下文的遵循。

相关：
- [[04_Embodied-AI/VLA/VLA-architecture|VLA 架构要素]] — action expert 在 VLA 中的具体实现
- [[05_Papers/articles/pi0-7|pi0.7 论文笔记]] — pi0.7 中 flow matching action expert 的实例
