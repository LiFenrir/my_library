---
title: Asynchronous Inference for Robot Control
description: 将世界模型的动作预测与机器人执行并行化，以隐藏推理延迟、实现高频闭环控制
tags:
  - embodied-ai
  - world-model
  - robot-control
  - real-time
  - inference
created: 2026-07-30
---

# Asynchronous Inference for Robot Control

**Asynchronous Inference for Robot Control** 是一种部署策略：在机器人执行当前动作块的同时，世界模型并行预测下一动作块，从而重叠计算与物理执行，隐藏推理延迟。

## Problem

自回归视频-动作世界模型每步都需要生成视频 token 和动作 token，推理延迟可能违反实时控制要求。同步模式下，机器人必须等待模型生成完下一批动作才能继续执行，导致控制频率下降。

## Core Idea

将推理与执行拆分为两条并行分支：

- **Branch A（执行）**：机器人按已生成的动作块 $a_{t:t+K-1}$ 运行；
- **Branch B（推理）**：同时基于最新观测预测下一视频块 $\hat{z}_{t+1:t+K}$ 和动作块 $a_{t+K:t+2K-1}$。

## Naive Asynchronous Pitfall

简单实现会把上一时刻生成的预测视频 $\hat{z}_t$ 直接缓存进 KV，作为预测 $\hat{z}_{t+1}$ 的条件。但由于视频生成模型偏好时间平滑，它倾向于"延续"自己生成的幻想视频，忽略最新的真实观测 $z_{t-1}$，最终导致开环退化和轨迹漂移。

## Forward Dynamics Grounding

解决方案是在推理分支中加入 **Forward Dynamics Model (FDM)** 接地步骤：

1. 使用最新真实反馈 $z_{t-1}$ 和正在执行的动作 $a_t$；
2. 通过 FDM 重新生成当前时刻的 grounded 预测 $\hat{z}_t$；
3. 用这个与真实反馈对齐的预测替代陈旧预测，再生成 $\hat{z}_{t+1}$。

这样强制模型在预测未来前重新与环境反馈对齐，维持闭环响应能力。

## 优缺点

- **优点**：
  - 显著提升控制频率；
  - 不牺牲自回归闭环校正能力（配合 FDM）；
  - 可与 KV cache、部分去噪等技术叠加。
- **缺点/局限**：
  - 需要额外 FDM 接地机制避免漂移；
  - 系统设计更复杂，涉及线程安全队列和时序同步；
  - 对动作执行时间波动敏感。

## Related Concepts

- [[03_Robotics/Control/Forward-Dynamics|Forward Dynamics]] — 异步推理中用于接地预测
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 使用 KV cache 的自回归世界模型天然支持异步推理
- [[04_Embodied-AI/VLA/Real-time-Action-Chunking|Real-Time Action Chunking]] — 同样处理推理延迟，但侧重于训练时模拟延迟
- [[04_Embodied-AI/World-Model/Noisy-History-Augmentation|Noisy History Augmentation]] — 常与异步推理配合加速视频生成

## Papers

- [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]] — 第 3.4 节提出 FDM 接地的异步推理管道
