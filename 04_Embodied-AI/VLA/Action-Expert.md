---
title: Action Expert
description: VLA 中专司将视觉语言表示转换为机器人动作序列的轻量专家网络
tags:
  - embodied-ai
  - vla
  - architecture
  - robot-learning
created: 2026-07-28
---

# Action Expert

Action Expert 是 VLA 中**专门负责动作生成**的轻量级 Transformer 模块，通常叠加在 VLM backbone 之上。

## Core Idea

VLM backbone 处理视觉和语言信息，Action Expert 则关注这些多模态表示并生成连续动作。这种解耦使得：

- VLM 专注于感知与语义理解
- Action Expert 专注于动作分布建模
- 可独立优化动作生成速度与质量

## Typical Design

- **规模**：通常远小于 VLM backbone（如 860M vs 4B）
- **注意力**：Action token 可双向关注自身，也可关注 VLM backbone 激活
- **目标函数**：Flow Matching 或 Diffusion 损失

## Knowledge Insulation

为防止动作梯度破坏 VLM 的预训练表示，训练中常将 Action Expert 的梯度**隔离**，不反向传播到 VLM backbone。

## Related Concepts

- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — Action Expert 是 VLA 的核心组件
- [[04_Embodied-AI/VLA/Flow-based-VLA|Flow-based VLA]] — 使用流匹配目标的 Action Expert
- [[04_Embodied-AI/VLA/Knowledge-Insulation|Knowledge Insulation]] — 训练 Action Expert 时的常用技巧
- [[04_Embodied-AI/VLA/Action-Chunking|Action Chunking]] — Action Expert 通常输出动作块

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 860M 参数 action expert，输出 50 步动作块
