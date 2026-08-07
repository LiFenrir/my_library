---
title: "Real-Robot VLA Evaluation"
description: "面向真实机器人 VLA 策略的分布化评估方法论，强调时间-成功 CDF、置信区间与成对检验"
tags: [concept, embodied-ai, vla, evaluation, benchmarking]
created: 2026-07-30
---

# Real-Robot VLA Evaluation

**核心定义**：在真实机器人上评估 Vision-Language-Action（VLA）策略时，采用时间-成功分布、置信区间和成对检验等统计方法，替代简单的二元成功率和吞吐标量。

## 为什么需要

当前 VLA 真实机器人评估常见缺陷：

- 样本量小（$N \leq 25$ rollouts/condition），无法可靠区分策略；
- 仅报告二元成功率或吞吐（UPH/cycle time），信息损失大；
- 缺少置信区间和成对检验，排序噪声高。

## 核心方法

### 1. Time-to-Success CDF

将每次 rollout 记录为「首次成功所需时间」或「在时间内是否成功」，构造累积分布函数 $F(t)$：

- 同时反映**可靠性**（最终成功率，$F(t) \to 1$ 的高度）与**吞吐**（达到高成功率的快慢）；
- 硬失败表现为 $F(t) < 1$ 的渐近线。

### 2. 统计检验

- 报告置信区间；
- 使用成对检验（paired test）比较同一条件下不同策略；
- 避免仅依赖标量排名导致的不一致结论。

## 工程含义

- 真实机器人评估需要与临床/工业试验相当的样本量；
- 单一标量（成功率或 UPH）可能给出矛盾排序，应使用完整分布；
- 时间-成功 CDF 是更鲁棒的策略比较工具。

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — 评估对象
- [[04_Embodied-AI/VLA/VLA-Edge-Characterization|VLA Edge Characterization]] — 互补的延迟与部署评估

## 来源

- [[05_Papers/articles/phail|PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology]]
