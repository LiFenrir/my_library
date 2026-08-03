---
title: "Compositional World Model"
description: "将动力学预测与价值估计解耦，以分别优化构建可学习仿真环境的世界模型"
tags: [concept, embodied-ai, world-model, robot-rl]
created: 2026-07-29
---

# Compositional World Model

**核心定义**：Compositional World Model 将世界模型分解为**动力学模型（dynamics model）**和**价值模型（value model）**两个独立组件，各自采用最适合的架构和训练目标，从而构建可用于强化学习的可学习仿真环境。

## 两个组件

1. **Dynamics Model（动力学模型）**
   - 预测未来观测 $\hat{o}_{t+1:t+H}$ 给定历史观测和动作块
   - 通常基于高效视频扩散模型初始化
   - 需要精确的动作可控性

2. **Value Model（价值模型）**
   - 评估预测状态的进度/价值
   - 提供密集、对失败敏感的学习信号
   - 常从预训练 VLA backbone 初始化

## 优势

- 每个组件可独立优化架构和训练目标
- 动力学模型专注视觉真实感和动作一致性
- 价值模型专注评估和奖励信号
- 避免单一模型同时承担预测和评估的负担

## 在 RISE 中的应用

RISE 的 Compositional World Model：

- 动力学模型：从 Genie Envisioner 初始化，加入 action encoder
- 价值模型：从 π0.5 VLA 初始化，结合 progress regression 和 TD learning
- 在想象中生成 rollout，计算优势，优化策略

## 相关流程

- [[04_Embodied-AI/Robot-RL/policy-warm-up-for-world-model-rl|Policy Warm-up for World Model RL]] — 在真实经验上锚定策略
- [[04_Embodied-AI/Robot-RL/self-improving-robot-policy|Self-Improving Robot Policy]] — 基于 Compositional World Model 的持续优化循环

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/World-Model|World Model]] — Compositional World Model 是其实现形式
- [[01_Fundamentals/ML/Model-Based-Reinforcement-Learning|Model-Based Reinforcement Learning]] — 应用场景
- [[04_Embodied-AI/Robot-RL/Advantage-Conditioning|Advantage Conditioning]] — 从价值模型提取优势
- [[04_Embodied-AI/World-Model/task-centric-batching|Task-Centric Batching]] — 训练动力学模型时的采样策略

## 来源

- [[05_Papers/articles/rise|RISE: Self-Improving Robot Policy with Compositional World Model]]，第 II-A、III-A 节
