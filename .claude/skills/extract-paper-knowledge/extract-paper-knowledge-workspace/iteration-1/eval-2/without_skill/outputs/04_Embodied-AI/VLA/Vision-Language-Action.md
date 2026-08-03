---
title: "Vision-Language-Action"
description: "将视觉感知、自然语言指令与机器人动作生成统一在单一模型中的范式。"
tags: [vla, embodied-ai, robot-policy, multimodal]
created: 2026-07-28
---

# Vision-Language-Action (VLA)

VLA 将视觉观测、语言指令与动作生成统一到一个自回归多模态策略中。RT-2 最早将机器人动作表示为 VLM 的 token，OpenVLA 则提供了 7B 规模的开源实现。

## 核心要点

- 动作可被离散化为 token，与文本共享同一输出空间。
- 依赖大规模视觉-语言预训练提升泛化与语义理解。
- 在操作、导航、空中机器人等具身任务中已有大量变体。

## 相关方向

- [[Real-Time-VLA-Inference|实时 VLA 推理]] — 边缘设备上的延迟与调度优化
- [[Aerial-VLA|空中 VLA]] — 面向无人机等空中平台的 VLA
- [[Advantage-Reward-Modeling|优势奖励建模]] — 用相对优势改进长程操作策略
- [[Long-Horizon-Manipulation|长程操作]] — VLA 在长程任务中的应用

## 来源

- LiteVLA-H: 空中 VLA 的双速率推理调度
- ARM: 基于 GR00T-N1.5 的 VLA 策略精炼
