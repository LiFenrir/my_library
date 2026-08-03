---
title: Compositional Task Generalization
description: 机器人策略通过组合训练时见过的技能来解决全新任务的能力
tags:
  - embodied-ai
  - vla
  - generalization
  - robot-learning
created: 2026-07-28
---

# Compositional Task Generalization

Compositional Task Generalization 是指机器人策略能够**将训练时学到的基本技能重新组合，以解决从未见过的新任务**。

## Core Idea

不同于简单的语义泛化（如识别新对象标签），组合泛化要求模型理解任务结构，并将已有技能按新方式组合。例如，将“抓取”、“打开”、“放置”等技能组合成“使用空气炸锅”的新任务。

## Forms

- **Short-horizon composition**：简单新任务可直接通过语言提示完成
- **Long-horizon composition**：需要分步语言辅导或高层策略将子任务串联

## Enabling Factors

- 大规模多样化任务数据
- 详细的语言指令和子任务分解
- 强大的语言跟随能力
- 子目标图像提供的视觉提示

## Coaching to Autonomy

对于复杂新任务，可先通过人类语言“辅导”模型逐步执行；然后用这些辅导数据训练高层语言策略，使模型能够自主完成该任务。

## Related Concepts

- [[04_Embodied-AI/VLA/Diverse-Prompting-for-VLA|Diverse Prompting for VLA]] — 丰富的提示支持技能组合
- [[04_Embodied-AI/VLA/Coaching-for-VLAs|Coaching for VLAs]] — 通过语言辅导教授新任务
- [[04_Embodied-AI/VLA/Cross-embodiment-Generalization|Cross-embodiment Generalization]] — 另一种高级泛化能力

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 展示使用空气炸锅、烤面包机等新任务的组合泛化
