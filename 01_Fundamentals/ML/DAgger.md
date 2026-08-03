---
title: "DAgger (Dataset Aggregation)"
description: "通过迭代收集模型自身状态下专家纠正数据，减少模仿学习与测试分布差距的算法"
tags: [concept, fundamentals, ml, imitation-learning]
created: 2026-07-30
---

# DAgger (Dataset Aggregation)

**核心定义**：DAgger（Dataset Aggregation）是一种迭代式模仿学习算法，通过让专家在模型自身策略访问到的状态下提供动作标签，逐步扩展训练数据分布，缩小训练分布与测试分布的差距。

## 核心问题

标准行为克隆只在专家演示状态上训练，测试时模型会访问到训练分布之外的状态（复合误差）。DAgger 通过在模型 rollout 上收集专家纠正来解决这个问题。

## 算法流程

1. 初始化数据集 $\mathcal{D}$ 为专家演示；
2. 在 $\mathcal{D}$ 上训练策略 $\pi_1$；
3. 使用 $\pi_i$ 运行 rollout，收集访问到的状态；
4. 专家在这些状态下标注动作，加入 $\mathcal{D}$；
5. 重复直到策略收敛。

## 变体

- **Heuristic DAgger**：用启发式而非人类专家提供纠正信号，降低标注成本。

## 与其他概念的关系

- [[01_Fundamentals/ML/Imitation-Learning|Imitation Learning]] — DAgger 的框架
- [[01_Fundamentals/ML/Heuristic-DAgger|Heuristic DAgger]] — 低成本变体
- [[04_Embodied-AI/Robot-RL/Advantage-Reward-Modeling|Advantage Reward Modeling]] — 用学习信号替代专家标注的方向

## 来源

- Ross, Gordon & Bagnell, 2011, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning"
