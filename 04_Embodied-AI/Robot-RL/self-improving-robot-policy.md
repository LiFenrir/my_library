---
title: "Self-Improving Robot Policy"
description: "在可学习世界模型中通过想象 rollout 和策略优化形成闭环，持续提升机器人策略性能"
tags: [concept, embodied-ai, robot-rl, world-model, self-improvement]
created: 2026-07-30
---

# Self-Improving Robot Policy

**核心定义**：Self-Improving Robot Policy 指机器人策略在一个可学习世界模型中通过「生成想象轨迹 → 估计优势 → 优化策略」的闭环不断自我提升，而无需持续的真实世界交互。

## 核心循环

1. **世界模型生成想象 rollout**：Compositional World Model 合成未来观测和奖励/价值信号；
2. **优势估计**：价值模型为每个动作块分配密集学习信号；
3. **策略优化**：基于想象数据用 RL 或加权回归更新策略；
4. **迭代**：更新后的策略生成新的 rollout，循环继续。

## 优势

- 突破真实演示数据的覆盖限制；
- 在想象中探索失败恢复等分布外行为；
- 减少昂贵且危险的真实世界试错。

## 挑战

- 世界模型质量决定自提升上限；
- 模型偏差可能自我强化；
- 需要真实经验锚定策略分布（见 Policy Warm-up）。

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/compositional-world-model|Compositional World Model]] — 提供可学习仿真环境
- [[04_Embodied-AI/Robot-RL/policy-warm-up-for-world-model-rl|Policy Warm-up for World Model RL]] — 启动自提升前的准备
- [[04_Embodied-AI/Robot-RL/Advantage-Conditioning|Advantage Conditioning]] — 策略优化的信号形式

## 来源

- [[05_Papers/articles/rise|RISE: Self-Improving Robot Policy with Compositional World Model]]，第 III-C 节
