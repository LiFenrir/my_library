---
title: Reward Engineering Bottleneck
description: 长程机器人操作规模化部署中对高精度进度奖励模型的过度依赖所形成的工程瓶颈
tags:
  - embodied-ai
  - robot-rl
  - reward-design
  - long-horizon
  - vla
  - reward-engineering
created: 2026-07-30
---

# Reward Engineering Bottleneck

在长程机器人操作任务中，策略改进严重依赖高精度、高频率的进度奖励模型，这种依赖限制了 VLA 等策略在真实非结构化环境中的可扩展性与稳定性。

## Why

- 稀疏奖励难以提供足够的信用分配信号；
- 密集奖励需要任务特定的启发式或精确子任务分段；
- 现有方法为缓解信用分配问题而依赖高精度进度奖励模型，形成规模化瓶颈。

## Manifestations

1. **标注成本高**：连续绝对进度标注需要人类判断每帧完成百分比，主观性强、跨标注者一致性差。
2. **VLM 不可靠**：零样本视觉-语言模型缺乏空间几何 grounding，推理开销大，奖励信号非单调振荡。
3. **单调性假设过强**：将进度等同于时间顺序，用视频倒带等简化手段模拟回退，无法刻画真实非线性错误。
4. **子任务分段过粗**：丢失阶段内关键转换（如恢复、纠正），导致奖励错位和策略更新不稳定。

## Mitigation: Relative Advantage

ARM 提出的核心思路是将奖励建模从绝对进度转向相对优势：

- 只判断状态相对历史是推进、停滞还是回退；
- 三态标签降低认知负荷并提高一致性；
- 无需任务特定的进度函数，天然兼容非单调轨迹。

## Related Concepts

- [[Long-Horizon-Manipulation-Reward]] — 长程操作奖励设计的共性问题
- [[Advantage-Reward-Modeling]] — 相对优势奖励模型
- [[Tri-state-Advantage-Labeling]] — 低成本标注策略
- [[Vision-Language-Action]] — 受瓶颈影响的策略模型背景

## Papers

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]，第 1 节
