---
title: "组合任务泛化与语言教练"
description: "VLA 通过组合已有技能解决新任务，以及通过语言教练获取新能力的机制。"
tags: [embodied-ai, generalization, compositional-generalization, coaching, vla]
created: 2026-07-28
---

# 组合任务泛化与语言教练

组合泛化是通用机器人模型的核心能力：把训练中的技能以新方式组合，完成未见过的新任务。

## 组合泛化层级

- **短程新任务**：如擦拭耳机、转动风扇等，无需额外数据即可通过语言/图像提示直接完成。
- **长程新任务**：如“用空气炸锅烤红薯”，需要把多个子技能按新顺序组合。

## 语言教练（Language Coaching）

- 人类通过逐步子任务指令引导模型完成未见长程任务。
- 模型只需跟随语言，无需采集该任务的动作演示数据。
- 教练过程可记录为 (observation, task, subtask) 数据，用来训练一个**高层语言策略**。
- 高层策略随后能自动输出子任务指令，使模型自主完成新任务。

## 关键依赖

- 强大的语言跟随能力，能抵抗数据集偏置。
- 子任务指令和子目标图像作为 prompt，使低层策略聚焦当前步骤。
- 多模态上下文条件让模型在训练时见过“不同策略完成同一任务”的多种模式。

相关：
- [[04_Embodied-AI/VLA/multimodal-context-conditioning|VLA 的多模态上下文条件]]
- [[04_Embodied-AI/World-Model/subgoal-image-world-model|子目标图像世界模型]]
- [[05_Papers/articles/pi0-7|pi0.7 论文笔记]]
