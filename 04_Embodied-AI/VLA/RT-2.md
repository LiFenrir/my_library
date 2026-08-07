---
title: "RT-2"
description: "Google DeepMind 提出的视觉-语言-动作模型，将机器人动作表示为语言 token 进行端到端训练"
tags: [concept, embodied-ai, vla, google]
created: 2026-07-30
---

# RT-2

**核心定义**：RT-2（Robotic Transformer 2）是 Google DeepMind 提出的 Vision-Language-Action（VLA）模型，将机器人动作坐标离散化为文本 token，直接在预训练的视觉-语言模型（VLM）上进行端到端微调。

## 核心思想

- 将动作空间的每个维度离散化为 256 个 bin，每个 bin 对应一个文本 token；
-  thus 机器人动作生成被转化为下一个 token 预测问题；
- 直接继承 VLM 的语义理解与泛化能力。

## 优势

- **语义泛化**：能执行训练时未见过的物体类别和指令；
- **推理能力**：可利用 VLM 的常识推理进行简单规划；
- **数据效率**：相比纯模仿学习方法，能更好地利用异构机器人数据。

## 局限

- 动作离散化可能损失精度；
- 推理延迟较高；
- 主要适用于单臂操作任务。

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — RT-2 是 VLA 范式的奠基工作之一
- [[04_Embodied-AI/VLA/VLA-Architecture|VLA Architecture]] — RT-2 的离散动作 token 方案
- [[02_AI/VLM/large-mask-inpainting|Large Mask Inpainting]] — 与 RT 系列相关的其他视觉模型

## 来源

- Brohan et al., 2023, "RT-2: Vision-Language-Action Models"
