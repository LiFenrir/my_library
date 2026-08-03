---
title: "跨 embodiment 迁移"
description: "VLA 在不同机器人形态之间零样本迁移能力：形态差距、涌现策略、视觉子目标的作用。"
tags: [embodied-ai, generalization, cross-embodiment, vla]
created: 2026-07-28
---

# 跨 embodiment 迁移

跨 embodiment 迁移指策略在训练时未见过目标机器人/任务组合的情况下，直接把能力迁移到新机器人。

## 核心观察

- **零样本迁移**：pi0.7 在 UR5e 上完成衣物折叠，而训练数据全部来自另一种形态的双臂机器人。
- **形态差距（morphological gap）**：当目标机器人臂长、惯量、工作空间显著不同时，简单复制源机器人动作会失败。
- **涌现策略**：模型会针对目标形态自发选择不同策略。例如源机器人用双臂配合固定衣物，UR5e 则用单臂垂直抓取完成折叠。

## 促进因素

- **多机器人训练数据**：模型见过多种机器人，学会任务的结构而非具体关节轨迹。
- **子目标图像**：世界模型生成目标机器人视角下的未来视觉状态，提供跨形态的视觉类比。
- **语言/语义约束**：任务级和子任务级语言指令提供与具体形态无关的高层目标。

## 实践意义

- 可在便宜、易遥操作的平台上收集数据，再部署到重载工业臂。
- 降低为每种新机器人都采集演示数据的开销。

相关：
- [[04_Embodied-AI/World-Model/subgoal-image-world-model|子目标图像世界模型]]
- [[04_Embodied-AI/VLA/multimodal-context-conditioning|VLA 的多模态上下文条件]]
- [[05_Papers/articles/pi0-7|pi0.7 论文笔记]]
