---
title: "VLA 架构要素"
description: "Vision-Language-Action 模型通用架构：VLM 主干、视觉历史编码、动作专家、训练技巧，以 pi0.7 为例。"
tags: [embodied-ai, vla, architecture, pi0-7]
created: 2026-07-28
---

# VLA 架构要素

VLA 以预训练视觉-语言模型（VLM）为骨干，增加动作生成分支，把多模态观测映射到机器人动作块。

## 输入与输出

- 观测 $\mathbf{o}_t = [\mathbf{I}_t^1, \dots, \mathbf{I}_t^n, \mathbf{q}_t]$：多视角图像 + 本体感知。
- 历史观测 $\mathbf{o}_{t-T:t}$ 输入模型；输出未来动作块 $\mathbf{a}_{t:t+H}$。
- pi0.7 输出 50 步动作块，执行其中 15/25 步后再重新推理。

## 关键组件

- **VLM 主干**：pi0.7 使用 Gemma3 4B（含 400M 视觉编码器）初始化，负责语义理解与语言理解。
- **视觉历史编码器**：MEM 风格，对历史帧做时空压缩，输出固定数量 token。
- **Action Expert**：860M 参数的小 transformer， attending to VLM 中间激活；用 flow matching 目标生成连续动作。
- **知识绝缘（Knowledge Insulation）**：action expert 的梯度不回传 VLM，VLM 通过稳定的离散交叉熵（FAST tokens）训练，避免连续动作损失破坏视觉-语言表示。
- **动作 token 化（FAST tokens）**：训练时给 VLM 提供离散动作 token 监督，提高动作表示学习效率。
- **注意力掩码**：观测 token 与子目标图像 token 在块内双向注意力；文本 token 使用因果注意力。

## 训练与推理工程

- **实时动作分块（RTC）**：训练时模拟 0–12 步推理延迟，保证真实部署时动作平滑。
- **Control Mode**：在 prompt 中标识关节空间或末端执行器控制，训练时保留，测试时按任务选择。
- **CFG**：可对 prompt 任意部分（pi0.7 主要对 episode metadata）做 classifier-free guidance，强化期望行为模式。

相关：
- [[01_Fundamentals/ML/generative-models/flow-matching|Flow Matching 生成建模]] — action expert 的通用生成模型基础
- [[04_Embodied-AI/VLA/multimodal-context-conditioning|VLA 的多模态上下文条件]] — prompt 各组件如何进入模型
- [[04_Embodied-AI/World-Model/subgoal-image-world-model|子目标图像世界模型]] — 子目标图像来源
- [[05_Papers/articles/pi0-7|pi0.7 论文笔记]]
