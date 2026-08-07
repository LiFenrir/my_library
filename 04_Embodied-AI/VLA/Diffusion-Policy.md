---
title: "Diffusion Policy"
description: "将机器人动作生成建模为去噪扩散过程的模仿学习方法"
tags: [concept, embodied-ai, vla, imitation-learning, robot-learning, diffusion]
created: 2026-07-31
---

# Diffusion Policy

**核心定义**：Diffusion Policy 将机器人动作生成建模为去噪扩散过程，通过训练一个条件扩散模型，从噪声中逐步去噪生成平滑、多模态的机器人动作序列。

## 关键优势

1. **多模态动作分布**：能够表达同一状态下多个合理动作；
2. **平滑动作输出**：扩散过程天然生成连续平滑轨迹；
3. **高精度操作**：在接触丰富的操作任务中表现优异。

## 与 VLA 的关系

Diffusion Policy 的动作生成思想被后续 VLA 和机器人策略学习广泛借鉴，例如使用扩散模型作为动作头。

## 与其他概念的关系

- [[02_AI/Generative-Models/Flow-Matching|Flow Matching]] — 与扩散模型相关的生成方法
- [[01_Fundamentals/ML/Imitation-Learning|Imitation Learning]] — Diffusion Policy 的训练范式
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — 动作生成可与 VLA 架构结合

## 来源

- [[05_Papers/articles/h2r|Human-to-Robot Data Augmentation]]
