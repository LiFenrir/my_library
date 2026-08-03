---
title: "Action Chunking and RTC"
description: "VLA 推理技术：一次性生成未来多步动作块以减少推理频率，并通过训练时实时动作分块（RTC）补偿推理延迟。"
tags: [concept, embodied-ai, vla, inference, real-time, robot-policy]
created: 2026-07-28
---

# Action Chunking and RTC

核心定义：**Action Chunking** 指策略每次推理生成一个连续动作块（action chunk，例如 50 步），但实际只执行其中前 $\hat{H}$ 步（例如 15 或 25 步），从而降低高频推理开销并提高动作时间一致性。**RTC（Real-Time Action Chunking）** 进一步在训练时模拟不同推理延迟，使模型学会在动作块被部分执行后再生成新块，补偿真实部署中的延迟。

## 原理

1. **动作块生成**：策略输出固定长度动作序列 $\mathbf{a}_{t:t+H}$。
2. **部分执行**：每次只执行前 $\hat{H} < H$ 步，避免频繁调用模型。
3. **训练时延迟模拟**：在训练时随机模拟 0–12 步的推理延迟（对应 50Hz 下最多 240ms），让模型学习在部分动作已被执行、状态已变化的情况下生成后续动作。
4. **异步推理**：子目标图像、高层子任务指令与 VLA 推理可在不同线程异步进行，进一步降低有效延迟。

## 关键参数

| 参数 | 含义 | 典型值 |
|------|------|--------|
| $H$ | 动作块总长度 | 50 步 |
| $\hat{H}$ | 每次执行步数 | 15 / 25 步 |
| 去噪步数 | flow matching 采样步数 | 5 步 |
| 最大模拟延迟 | RTC 训练时延迟 | 12 步 @ 50Hz |

## 优缺点

- 优点：
  - 显著降低单位时间内的模型调用次数。
  - 动作块内时间一致性更好。
  - RTC 让策略对真实推理延迟更鲁棒。
- 缺点 / 局限：
  - 动作块过长会放大误差累积。
  - 训练时需要精确模拟延迟和状态偏移。
  - 不同控制频率（如 20Hz vs 50Hz）需要相应调整参数。

## 与其他概念的关系

- [[vla-architecture|VLA Architecture]] — action chunking 是 VLA 推理的标准组件。
- [[02_AI/Flow-Matching-action-expert|Flow Matching Action Expert]] — 生成动作块的具体实现。
- [[prompt-conditioning-for-vla|Prompt Conditioning for VLA]] — 上下文在每次重新生成动作块时刷新。

## 来源

- [[05_Papers/articles/pi0-7|π0.7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities]] — Sec. VI-B, Sec. VII
