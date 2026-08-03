---
title: "Latent Action"
description: "在潜在空间中表示动作的低维紧凑动作表示"
tags: [concept, embodied-ai, world-model, representation-learning]
created: 2026-07-29
---

# Latent Action

**核心定义**：Latent Action 是在潜在空间中表示动作的低维、紧凑动作表示。与原始关节命令或末端执行器位姿不同，latent action 通过无监督或自监督方式从数据中学习，捕捉动作的核心变化模式。

## 典型方法

- 从视频中学习潜在动作（无需动作标注）
- 用 VAE 或扩散模型编码动作序列
- 在 world model 中与视觉状态联合建模

## 优势

- 可利用大量无动作标签的视频数据
- 动作表示紧凑，降低策略学习难度
- 有助于跨 embodiment 迁移

## 代表工作

- Motus：unified latent action world model
- Latent Action Pretraining from Videos
- Robo-Dopamine 等 hop-based 方法

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — latent action 常与 WAM 联合学习
- [[04_Embodied-AI/Sim2Real/cross-embodiment-transfer|Cross-Embodiment Transfer]] — latent action 有助于跨 embodiment

## 来源

- [[05_Papers/articles/motus|Motus: A Unified Latent Action World Model]]
