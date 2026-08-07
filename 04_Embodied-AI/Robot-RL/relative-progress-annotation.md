---
title: "Relative Progress Annotation"
description: "用相对推进/回退/停滞三态标签替代绝对进度标注的低成本奖励标注方法"
tags: [concept, embodied-ai, robot-rl, data-annotation]
created: 2026-07-29
---

# Relative Progress Annotation

**核心定义**：Relative Progress Annotation 是一种低成本的机器人奖励标注方法，用三态分类（推进 / 回退 / 停滞）替代传统的连续绝对进度标注，从而降低标注者认知负担并提高跨标注者一致性。

## 三态定义

| 标签 | 含义 | 示例 |
|------|------|------|
| +1 Progressive | 状态有效向目标推进 | 机器人成功抓取物体并靠近目标位置 |
| -1 Regressive | 状态偏离目标或遇到错误 | 物体滑落、碰撞、错误操作 |
| 0 Stagnant | 没有实质性进展 | 等待、空闲、微小抖动 |

## 相比绝对进度标注的优势

- **认知负荷低**：标注者不需要判断具体进度百分比
- **一致性高**：三态分类的跨标注者一致性优于连续值
- **任务无关**：不需要为每个任务定义进度函数
- **兼容非单调行为**：可以自然处理回退、恢复、重试

## 冷启动与扩展

1. 先用少量人工三态标注训练初始模型
2. 用训练好的模型对大量未标注轨迹进行推理，生成伪标签
3. 用伪标签数据进一步训练，实现规模化扩展

## 与其他概念的关系

- [[04_Embodied-AI/Robot-RL/Advantage-Reward-Modeling|Advantage Reward Modelin[[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]] — 使用三态标签作为训练信号
- [[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]]|Long-Horizon Manipulatio[[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]] — 典型应用场景
- [[04_Embodied-AI/Robot-RL/Reward-Engineering-Bottleneck|Reward Engineering Bottlenec[[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]] — 本方法试图解决的问题

## 来源

- [[05_Papers/articles/arm|ARM: Advantage Reward Modeling for Long-Horizon Manipulatio[[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]]，第 3.2.2 节
