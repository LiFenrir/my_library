---
title: Real-time Action Chunking
description: 在训练时模拟推理延迟，使动作块策略能够在真实实时控制中保持平滑的技术
tags:
  - embodied-ai
  - vla
  - robot-control
  - real-time
created: 2026-07-28
---

# Real-time Action Chunking

Real-time Action Chunking（RTC）是一种使**动作块策略在存在推理延迟的真实机器人系统中保持实时控制**的技术。

## Core Idea

动作块模型在训练时假设可以立即获得新动作，但实际推理需要数十到数百毫秒。RTC 在训练时模拟这种延迟，使模型学会在延迟条件下生成平滑且有效的动作轨迹。

## Training-Time RTC

在训练时，将未来动作的输入延迟 0 到若干时间步，模拟推理等待期间机器人继续执行旧动作块的情形。这样模型学会根据“过时”的动作上下文生成下一步动作。

## Benefits

- **无额外推理开销**：训练时 RTC 不增加运行延迟
- **平滑性**：模型生成的动作能自然衔接延迟期间执行的动作
- **高频率控制**：支持 20–50 Hz 机器人控制

## Key Parameters

- **最大模拟延迟**：如 0–12 步（对应 240ms @ 50Hz）
- **动作块长度 $H$**
- **执行长度 $\hat{H}$**

## Related Concepts

- [[Action-Chunking|Action Chunking]] — RTC 的基础技术
- [[Action-Expert|Action Expert]] — 生成动作块的模块
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]] — 使用 RTC 的机器人策略

## 补充：来自 [[04_Embodied-AI/VLA/Real-time-Action-Chunking|real-time-action-chunking（已合并）]]

- 执行时重叠使用新旧 action chunk，减少抖动。
- **优点**：减少实际部署中的动作抖动；允许使用更大的 chunk 而不牺牲响应性；对实时控制友好。
- **局限**：训练更复杂；延迟模拟参数需要针对机器人频率调整。

### 其他来源

- Kevin Black et al., *Training-Time Action Conditioning for Efficient Real-Time Chunking*, arXiv:2512.05964
- Kevin Black et al., *Real-Time Execution of Action Chunking Flow Policies*, arXiv:2506.07339

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 使用训练时 RTC 实现 50Hz 实时控制
