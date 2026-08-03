---
title: "ACT"
description: "将连续动作序列建模为离散动作块、用于机器人模仿学习的 Transformer 模型"
tags: [concept, embodied-ai, vla, imitation-learning, robot-learning]
created: 2026-07-31
---

# ACT

**核心定义**：ACT（Action Chunking with Transformers）是一种机器人模仿学习方法，通过 Transformer 模型一次性预测未来一段连续动作块（action chunk），并使用残差策略处理时序累积误差，适用于高精度的机器人操作任务。

## 关键思想

1. **动作块输出**：模型每步预测未来 $k$ 个动作，减少推理频率；
2. **Transformer 架构**：编码器-解码器结构，结合图像观测与语言指令；
3. **残差策略**：在动作块执行过程中逐步修正，降低 compounding error。

## 与 Action Chunking 的关系

ACT 是实现动作块预测的代表性方法之一，影响了后续 VLA 中的动作块设计。

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Action-Chunking|Action Chunking]] — ACT 的核心机制
- [[01_Fundamentals/ML/Imitation-Learning|Imitation Learning]] — ACT 的训练范式
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — ACT 可视为早期 VLA 风格的动作生成方法

## 来源

- [[05_Papers/articles/h2r|Human-to-Robot Data Augmentation]]
