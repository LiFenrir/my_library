---
title: "Long-Horizon Manipulation"
description: "需要多个子任务、长时间执行和复杂物体交互的机器人操作问题"
tags: [concept, embodied-ai, robotics, manipulation]
created: 2026-07-29
---

# Long-Horizon Manipulation

**核心定义**：Long-Horizon Manipulation 指需要多个连续步骤、长时间执行（通常数分钟）、涉及复杂物体交互（如 deformable objects、液体、装配）的机器人操作任务。

## 典型挑战

- **稀疏奖励**：只有最终成功/失败信号，中间步骤缺乏监督
- **信用分配**：难以确定哪些动作对最终成功最关键
- **非单调行为**：真实执行中常出现回退、重试、恢复
- **复合错误**：早期小错误会在后续步骤中放大
- **数据多样性**：需要大量高质量演示

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

## 与其他概念的关系

- [[04_Embodied-AI/Robot-RL/Advantage-Reward-Modeling|Advantage Reward Modeling]] — 解决长程任务信用分配问题
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 可端到端执行长程语言指令
- [[04_Embodied-AI/Robot-Planning/Hierarchical-Planning|Hierarchical Planning]] — 长程任务的常见分解策略

## 来源

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulation]]，第 1、4.1 节
