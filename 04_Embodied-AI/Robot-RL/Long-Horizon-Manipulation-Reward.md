---
title: Long-Horizon Manipulation Reward
description: 长程机器人操作任务中奖励设计的核心矛盾与从绝对进度到相对优势的范式转移
tags:
  - embodied-ai
  - robot-rl
  - reward-design
  - long-horizon
  - manipulation
created: 2026-07-28
---

# Long-Horizon Manipulation Reward

长程机器人操作任务（如折叠毛巾、装配、整理）需要持续、细粒度的奖励信号来引导策略跨越多个子阶段。

## Why

- **稀疏奖励**（如最终成功/失败）信用分配困难，收敛慢；
- **密集奖励**需要人工设计任务相关启发式或精确子任务分段，扩展性差；
- 真实演示常包含非单调行为：回退、重试、恢复、临时调整。

这些矛盾构成了机器人学习规模化部署中的 **Reward Engineering Bottleneck**。

## Absolute Progress 的局限

以“完成了多少百分比”为核心的方法存在以下问题：

1. **VLM 不可靠**：零样本视觉-语言模型缺乏空间几何 grounding，产生抖动、低精度信号；
2. **量化歧义**：失败状态难以用单一数值表达；
3. **单调性假设过强**：视频倒带等简化手段无法刻画真实非线性错误；
4. **子任务分段过粗**：丢失阶段内关键转换（如恢复动作），导致奖励错位。

## Relative Advantage 范式

将奖励定义为“相对于历史状态的进展”，而非“相对于全局目标的绝对进度”：

- 推进、回退、停滞三种基本类别已足以提供有效监督；
- 不依赖任务特定的进度定义；
- 天然兼容非单调轨迹。

ARM 是这一范式的具体实现：用 [[Advantage-Reward-Modeling|相对优势模型]] 估计局部变化，再用 [[Global-Progress-Reconstruction|全局重建]] 得到密集进度曲线。

## Related Concepts

- [[Advantage-Reward-Modeling]]
- [[Tri-state-Advantage-Labeling]]
- [[Global-Progress-Reconstruction]]
- [[Advantage-Weighted-Behavior-Cloning]]
- [[Imitation-Learning]] / [[Offline-Reinforcement-Learning]]
- [[Vision-Language-Action]]

## Papers

- [[arm]] — ARM: Advantage Reward Modeling for Long-Horizon Manipulation
