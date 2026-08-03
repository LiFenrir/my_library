---
title: "Speculative Asynchronous Inference"
description: "在机器人执行当前动作块的同时预去噪下一步世界模型预测，将扩散/流模型的去噪延迟隐藏到物理执行时间中"
tags: [concept, embodied-ai, world-model, diffusion, latency, asynchronous]
created: 2026-07-30
---

# Speculative Asynchronous Inference (SAI)

**核心定义**：Speculative Asynchronous Inference 是一种机器人世界模型推理调度策略：在机器人执行当前动作块的同时，提前开始下一步未来观测与动作的扩散/流去噪过程，从而将原本阻塞控制循环的去噪延迟隐藏到物理执行时间中。

## 为什么需要

视频扩散/流世界模型每步推理需要多步去噪（如 10–50 步），产生显著延迟。若采用同步方式：

- 先等待模型生成动作，再执行动作；
- 控制频率被模型推理时间严重限制。

SAI 利用动作块执行期间的空闲计算资源，提前启动下一步生成。

## 核心机制

### 1. 执行与推理并行

当前动作块 $a_{t:t+H}$ 发送到机器人执行的同时，模型开始基于最新观测预测下一步 $a_{t+H:t+2H}$。

### 2. 部分去噪

由于下一步的真实未来观测尚未到来，SAI 使用当前模型预测作为「投机」起点，完成大部分去噪步。当真实观测到达后，只需少量修正步即可输出最终动作。

### 3. 回退机制

若预测误差过大，可回退到同步模式或重新去噪。

## 效果

DexWorldModel 报告 SAI 可降低约 **50%** 的阻塞延迟。

## 优缺点

- **优点**：显著提升控制频率，尤其适合动作块较长的场景；
- **缺点/局限**：依赖动作块执行时间足够覆盖去噪时间；预测误差可能累积。

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/causal-latent-world-model|Causal Latent World Model]] — DexWorldModel 的具体实现
- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — SAI 面向的模型范式
- [[04_Embodied-AI/World-Model/Asynchronous-Inference-for-Robot-Control|Asynchronous Inference for Robot Control]] — 同一大方向下的另一种异步方案

## 来源

- [[05_Papers/articles/dexworldmodel|DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks]]
