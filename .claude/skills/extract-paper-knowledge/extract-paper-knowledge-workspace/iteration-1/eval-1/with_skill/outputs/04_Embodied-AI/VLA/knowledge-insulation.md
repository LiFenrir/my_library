---
title: "Knowledge Insulation"
description: "VLA 训练技巧：用离散视觉-语言监督训练 VLM 骨干，同时阻止动作专家的梯度回传，以保持骨干稳定并提升泛化。"
tags: [concept, embodied-ai, vla, training, vlm, robot-policy]
created: 2026-07-28
---

# Knowledge Insulation

核心定义：**Knowledge Insulation（KI）** 是一种训练 VLA 的稳定化技巧：VLM 骨干主要使用离散视觉-语言任务（如 FAST tokens 的交叉熵损失）进行监督，而 action expert 虽然 attend 到骨干的所有激活，但其损失梯度不反向传播到 VLM 骨干，从而“隔离”语义知识与动作学习。

## 原理

1. **梯度隔离**：action expert 的梯度只更新 action expert 自身及其输入投影，不流入 VLM 骨干。
2. **离散监督稳定 VLM**：VLM 骨干通过相对稳定的离散 token 预测任务（如图像/文本重建、FAST action tokenization）进行训练，避免了连续动作回归可能带来的噪声梯度破坏预训练表示。
3. **表示迁移**：由于 action expert 可以读取骨干所有层激活，VLM 学到的语义、空间、物体知识仍能被动作头利用。

## 作用

- 保护预训练 VLM 的开放词汇和常识能力不被机器人动作数据“带偏”。
- 让动作头和语义骨干各自使用适合自身的损失函数和优化动态。
- 通常与 flow matching / diffusion action expert 配合使用。

## 优缺点

- 优点：
  - 训练更稳定，减少灾难性遗忘。
  - VLM 可保持较强的语言跟随和视觉理解能力。
  - 便于分别扩展骨干和动作头规模。
- 缺点 / 局限：
  - 动作专家无法直接微调骨干表征来适应机器人任务，可能限制端到端优化。
  - 需要额外的离散监督信号（如 FAST tokens）和对应数据。

## 与其他概念的关系

- [[vla-architecture|VLA Architecture]] — KI 是 VLA 训练 recipe 的一部分。
- [[02_AI/Flow-Matching-action-expert|Flow Matching Action Expert]] — KI 常与 flow matching action expert 一起使用。
- [[prompt-conditioning-for-vla|Prompt Conditioning for VLA]] — 共同构成 π0.7 的训练与提示范式。

## 来源

- [[05_Papers/articles/pi0-7|π0.7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities]] — Sec. III
