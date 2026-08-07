---
title: "Long-Horizon Manipulation Reward"
description: "长程机器人操作任务中奖励设计的核心矛盾与从绝对进度到相对优势的范式转移"
aliases:
  - Long-Horizon Manipulation
tags:
  - embodied-ai
  - robot-rl
  - reward-design
  - long-horizon
  - manipulation
  - concept
created: 2026-07-28
---

# Long-Horizon Manipulation Reward

长程机器人操作任务（如折叠毛巾、装配、整理）需要持续、细粒度的奖励信号来引导策略跨越多个子阶段。

## 长程操作的核心挑战

- **稀疏奖励**：只有最终成功/失败信号，中间步骤缺乏监督
- **信用分配**：难以确定哪些动作对最终成功最关键
- **非单调行为**：真实执行中常出现回退、重试、恢复
- **复合错误**：早期小错误会在后续步骤中放大
- **数据多样性**：需要大量高质量演示

## 绝对进度的局限

以“完成了多少百分比”为核心的方法存在以下问题：

1. **VLM 不可靠**：零样本视觉-语言模型缺乏空间几何 grounding，产生抖动、低精度信号
2. **量化歧义**：失败状态难以用单一数值表达
3. **单调性假设过强**：视频倒带等简化手段无法刻画真实非线性错误
4. **子任务分段过粗**：丢失阶段内关键转换（如恢复动作），导致奖励错位

## 相对优势范式

将奖励定义为“相对于历史状态的进展”，而非“相对于全局目标的绝对进度”：

- 推进、回退、停滞三种基本类别已足以提供有效监督
- 不依赖任务特定的进度定义
- 天然兼容非单调轨迹

ARM 是这一范式的具体实现：用 [[04_Embodied-AI/Robot-RL/Advantage-Reward-Modeling|相对优势模型]] 估计局部变化，再用 [[04_Embodied-AI/Robot-RL/Global-Progress-Reconstruction|全局重建]] 得到密集进度曲线。

## 常见方法

| 方法 | 代表工作 | 核心思想 |
|------|---------|---------|
| 分层策略 | HiPAB, HULC | 高层规划 + 低层执行 |
| 子任务标注 | SARM | 人工定义子任务边界 |
| 相对优势奖励 | ARM | 用三态相对优势生成密集奖励 |
| 强化学习 | RECAP | 从自主经验中改进 |
| VLA | π0.7, OpenVLA | 大规模预训练 + 上下文条件 |

## 与 Short-Horizon 操作的区别

- Short-horizon：单步或几步内完成，如抓取、放置
- Long-horizon：需要数十到数百步，涉及工具使用、折叠、装配等

## Related Concepts

- [[04_Embodied-AI/Robot-RL/Advantage-Reward-Modeling|Advantage Reward Modeling]] — 解决长程任务信用分配问题
- [[04_Embodied-AI/Robot-RL/Global-Progress-Reconstruction|Global Progress Reconstruction]]
- [[04_Embodied-AI/Robot-RL/Tri-state-Advantage-Labeling|Tri-state Advantage Labeling]]
- [[04_Embodied-AI/Robot-RL/Advantage-Weighted-Behavior-Cloning|Advantage-Weighted Behavior Cloning]]
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]] — 可端到端执行长程语言指令
- [[04_Embodied-AI/Robot-Planning/Hierarchical-Planning|Hierarchical Planning]] — 长程任务的常见分解策略

## Papers

- [[05_Papers/notes/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]
