---
title: Vision-Language-Action
description: 将视觉感知、语言理解与机器人动作生成统一在单一模型中的具身智能范式。
tags:
  - embodied-ai
  - vla
  - robotics
  - concept
created: 2026-07-28
---

# Vision-Language-Action (VLA)

VLA 是将**视觉感知、自然语言条件、机器人动作生成**统一在单一多模态模型中的策略范式。

## Why

传统机器人 pipeline 把感知、理解、规划、控制拆成独立模块，接口脆弱且难以利用互联网规模的视觉-语言先验。VLA 通过把动作也表示成语言模型的 token，让预训练 VLM 直接输出可执行动作。

## Core Idea

把机器人控制问题建模为条件语言建模：

```
P(a_t | I_t, g; θ)
```

- `I_t`：当前视觉观测
- `g`：自然语言目标/指令
- `a_t`：动作序列（被离散化为 token）

模型在一个端到端目标下同时学习视觉 grounding、语义理解和动作生成。

## How It Works

1. **Vision encoder**：将 RGB 图像编码为视觉 token。
2. **Multimodal transformer**：融合视觉 token 与文本提示。
3. **Action head / token decoder**：自回归地生成动作 token。
4. **De-tokenization**：将离散动作 token 映射回连续控制量（如线速度、角速度、关节位置）。

## Related Concepts

- [[Action-Tokenization|Action Tokenization]] — 连续动作如何离散化为 token
- [[Edge-VLA|Edge VLA]] — 面向嵌入式平台的轻量 VLA
- [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘 VLA 的延迟特征
- [[04_Embodied-AI/index|Embodied AI]] — 具身智能总览

## Papers

- [[05_Papers/articles/litevla-edge|LiteVLA-Edge]] — Jetson Orin 上的量化本地 VLA
- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 双速率边缘 VLA 调度
- [[OpenVLA]] — 7B 开源通用 VLA
- [[RT-2]] — 将 web 知识迁移到机器人控制

## Engineering

- 动作 token 设计直接影响控制精度与延迟。
- 模型规模、量化精度、推理运行时共同决定边缘部署可行性。
- ROS 2 等中间件常用于把 VLA 输出桥接到真实执行器。

## Questions

- 动作 token 空间如何平衡表达力与解码效率？
- 大模型通用性 vs. 小模型实时性如何权衡？
- 多模态 pre-fill 成本是边缘 VLA 的主要瓶颈吗？
