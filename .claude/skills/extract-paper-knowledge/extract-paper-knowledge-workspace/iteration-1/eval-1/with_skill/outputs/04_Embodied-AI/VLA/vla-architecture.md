---
title: "VLA Architecture"
description: "Vision-Language-Action（VLA）模型的通用架构：在预训练 VLM 骨干上附加 action expert，实现视觉-语言-动作的统一策略。"
tags: [concept, embodied-ai, vla, architecture, robot-policy]
created: 2026-07-28
---

# VLA Architecture

核心定义：**Vision-Language-Action（VLA）模型** 是一种将预训练视觉-语言模型（VLM）适配到机器人控制的通用架构。它把机器人轨迹中的观测和动作与语言指令统一到一个序列模型中，通过生成式动作头（action expert）输出未来动作。

## 原理

1. **VLM 骨干**：通常从一个预训练的视觉-语言模型初始化（如 Gemma、PaLI 等），负责理解图像、语言和高层语义。
2. **观测编码**：
   - 多视角相机图像 $\mathbf{I}_t^i$ 经视觉编码器压缩成 token。
   - 本体感知状态 $\mathbf{q}_t$（关节角、末端位姿等）线性投影为 token 后输入骨干。
   - 历史观测 $\mathbf{o}_{t-T:t}$ 可通过视频历史编码器压缩，保证不同历史长度下 token 数固定。
3. **Action Expert**：一个较小的 transformer，通过 cross-attention 读取 VLM 骨干激活，并预测动作块 $\mathbf{a}_{t:t+H}$。
4. **训练目标**：最大化条件动作似然，常用 flow matching 或 diffusion 目标捕捉动作多峰性。
5. **注意力模式**：观测 token 与目标图像 token 常用双向注意力，文本 prompt 用因果注意力，动作 token 之间双向注意力并可 attend 到骨干激活。

## 关键组件

| 组件 | 作用 | 典型设计 |
|------|------|----------|
| Vision Encoder | 提取视觉特征 | 预训练 ViT，处理多视角图像 |
| VLM Backbone | 融合视觉-语言-状态语义 | 4B–7B transformer |
| Action Expert | 生成动作块 | 小 transformer + flow matching |
| History Encoder | 压缩时序观测 | 时间+空间压缩，固定 token 数 |
| Proprioception Embedding | 编码机器人状态 | 线性投影或离散 token |

## 优缺点

- 优点：
  - 利用预训练 VLM 的开放词汇、语义理解和世界知识。
  - 统一了感知、语言理解与动作生成，便于多任务、多机器人训练。
  - 动作专家可灵活替换为 diffusion、flow matching 或自回归头。
- 缺点 / 局限：
  - VLM 与机器人动作域之间存在分布偏移，需要精心设计训练 recipe。
  - 大模型推理延迟高，需要历史压缩、action expert 解耦等工程优化。
  - 对数据质量和提示设计敏感。

## 与其他概念的关系

- [[02_AI/Flow-Matching-action-expert|Flow Matching Action Expert]] — VLA 的动作生成头常用方法。
- [[prompt-conditioning-for-vla|Prompt Conditioning for VLA]] — 决定 VLA 输入上下文的多模态提示设计。
- [[knowledge-insulation|Knowledge Insulation]] — 稳定训练 VLA 的常用技巧。
- [[action-chunking-and-rtc|Action Chunking and RTC]] — VLA 推理时减少延迟、保持平滑的关键工程方法。

## 来源

- [[05_Papers/articles/pi0-7|π0.7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities]] — Sec. III, Sec. VI-B
