---
title: Cross-embodiment Generalization
description: 机器人策略在未见过的机器人形态上直接执行训练任务的能力
tags:
  - embodied-ai
  - vla
  - generalization
  - robot-learning
created: 2026-07-28
---

# Cross-embodiment Generalization

Cross-embodiment Generalization 是指机器人策略**在训练时未见过的新机器人形态上直接执行任务**的能力。

## Core Idea

不同机器人可能拥有不同的臂长、自由度、夹爪形态和动力学特性。跨 embodiment 泛化要求策略从训练数据中提取任务语义和运动学无关的技能，并在目标形态上重新发现合适的执行策略。

## Key Factors

- **任务语义理解**：理解“做什么”独立于“怎么做”
- **形态无关表示**：从视觉和语言中提取与具体机器人无关的信息
- **策略组合**：根据目标形态调整动作策略

## Levels of Generalization

1. **同构形态**：仅尺寸、安装位置不同
2. **异构但能力相近**：单臂 vs 双臂静态平台
3. **显著形态差异**：轻量臂 vs 工业重载臂

## Emergent Strategies

强跨 embodiment 策略不仅复制源机器人动作，还会发现适合目标形态的新策略（如用单臂 pick-and-place 替代双臂协作）。

## Enabling Techniques

- 大规模跨机器人数据集
- 多模态提示（语言、子目标图像）
- 世界模型生成的目标机器人视角子目标

## Related Concepts

- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 具备跨 embodiment 泛化潜力的模型
- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]] — 通过视觉目标帮助跨形态迁移
- [[04_Embodied-AI/VLA/Compositional-Task-Generalization|Compositional Task Generalization]] — 另一种 VLA 高级泛化能力

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 实现 zero-shot 将灵巧折叠技能从静态双臂平台迁移到 UR5e 工业臂
