---
title: "Policy Warm-up for World Model RL"
description: "在启动世界模型中的自提升循环前，先在真实经验上微调策略以锚定行为分布并注入优势条件能力"
tags: [concept, embodied-ai, robot-rl, world-model, policy-initialization]
created: 2026-07-30
---

# Policy Warm-up for World Model RL

**核心定义**：Policy Warm-up 是在启动世界模型自提升循环之前，先在少量真实机器人经验上微调策略的阶段，目的是将策略锚定到实际行为分布，并赋予其基于优势条件（advantage conditioning）生成动作的能力。

## 为什么需要

直接用世界模型中的想象 rollout 训练冷启动策略存在问题：

- 策略可能远离真实世界的行为分布；
- 早期生成的想象轨迹质量低，导致错误累积；
- 预训练 VLA 通常是条件行为克隆，不理解优势/价值信号。

Warm-up 让策略先学会「如何利用优势条件生成合理动作」，再进入想象训练。

## 关键步骤

1. **收集真实 rollout**：在真实环境或高质量仿真中运行当前策略；
2. **计算优势信号**：用价值模型估计每段动作块的优势；
3. **优势条件微调**：将优势作为额外上下文输入，训练策略生成高优势动作。

## 在 RISE 中的应用

RISE 的 Policy Warm-up：

- 在 π0.5 VLA 基础上微调；
- 使用真实经验作为锚点；
- 训练策略根据估计优势调整动作生成。

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/compositional-world-model|Compositional World Model]] — Warm-up 后用于自提升循环
- [[04_Embodied-AI/Robot-RL/Advantage-Conditioning|Advantage Conditioning]] — Warm-up 注入的核心能力
- [[04_Embodied-AI/Robot-RL/Advantage-Reward-Modeling|Advantage Reward Modeling]] — 优势信号来源

## 来源

- [[05_Papers/articles/rise|RISE: Self-Improving Robot Policy with Compositional World Model]]，第 III-B 节
