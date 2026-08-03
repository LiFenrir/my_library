---
title: Action Chunking
description: 机器人策略一次预测并执行未来多步动作以降低推理频率、提升平滑性的技术
tags:
  - embodied-ai
  - vla
  - robot-control
  - inference
created: 2026-07-28
---

# Action Chunking

Action Chunking 是一种机器人策略**一次预测未来多步动作**并只执行其中一部分的技术，用于降低推理频率并提高动作平滑性。

## Core Idea

模型在时间 $t$ 预测一个动作块 $a_{t:t+H}$，但实际只执行前 $\hat{H}$ 步（$\hat{H} < H$）。经过 $\hat{H}$ 步后重新查询模型生成新的动作块。

## Benefits

- **降低推理频率**：减少模型调用次数
- **动作平滑性**：块内动作天然连贯
- **补偿延迟**：可与 Real-time Action Chunking（RTC）结合处理推理延迟

## Key Parameters

- **块长度 $H$**：一次预测的动作步数
- **执行长度 $\hat{H}$**：实际执行的步数
- **重叠 / 重规划周期**：$\hat{H}$ 决定重规划频率

## Trade-offs

- $H$ 越大：规划越长，但对环境动态变化响应越慢
- $\hat{H}$ 越小：重规划越频繁，实时性越好但计算成本越高
- 预测误差会在 chunk 内累积

## 补充：来自 [[04_Embodied-AI/VLA/Action-Chunking|action-chunking（已合并）]]

- 重叠执行方式（预测 $H$ 步、执行 $\hat{H}$ 步后重新推理）也称为 **temporal ensembling** 或 **receding horizon control**。
- **与 RTC 的关系**：[[04_Embodied-AI/VLA/Real-time-Action-Chunking|Real-Time Action Chunking]] 进一步解决推理延迟问题：在训练时模拟 0~12 步的推理延迟，使模型学会在存在延迟的情况下生成平滑轨迹。
- 详细推导见 [[05_Papers/articles/pi0-7|π0.7]] 第 III、VI-B 节。

## Related Concepts

- [[Real-time-Action-Chunking|Real-time Action Chunking]] — 处理推理延迟的动作块生成
- [[Action-Expert|Action Expert]] — 负责预测动作块的模块
- [[Vision-Language-Action-Model|Vision-Language-Action Model]] — 使用 Action Chunking 的机器人策略

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 预测 50 步动作块，执行 15 或 25 步
