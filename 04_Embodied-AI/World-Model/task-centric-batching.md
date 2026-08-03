---
title: "Task-Centric Batching"
description: "在训练动作可控世界模型时优先采样同任务不同动作的数据批次策略"
tags: [concept, embodied-ai, world-model, training]
created: 2026-07-29
---

# Task-Centric Batching

**核心定义**：Task-Centric Batching 是一种针对动作可控世界模型训练的数据采样策略。它在每个 batch 中优先采样来自少量任务、但包含多种不同动作的样本，以提高模型对动作的敏感性和可控性。

## 动机

训练可控世界模型时，如果每个 batch 包含太多不同任务和场景：

- 模型需要先学会区分场景，才能学习动作影响
- 动作多样性被场景多样性稀释
- 收敛慢、动作可控性差

Task-Centric Batching 通过"同场景、多动作"的采样方式，让模型更专注于学习动作如何影响未来状态。

## 与标准采样对比

| 策略 | 每个 batch 特点 | 效果 |
|------|----------------|------|
| 随机采样 | 多任务、多场景、多动作 | 场景理解优先，动作可控性差 |
| Task-Centric Batching | 少量任务、同场景、多动作 | 动作可控性更强 |

## 优缺点

- **优点**：提高动作可控性、加速任务特定微调、改善策略提升
- **缺点/局限**：可能牺牲场景泛化；需要 careful 的任务采样比例

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/compositional-world-model|Compositional World Model]] — RISE 中的训练策略
- [[04_Embodied-AI/World-Model/World-Model|World Model]] — 应用场景
- [[04_Embodied-AI/Robot-RL/policy-warm-up-for-world-model-rl|Policy Warm-up]] — 利用 Task-Centric Batching 训练后的动力学模型
- [[04_Embodied-AI/Robot-RL/self-improving-robot-policy|Self-Improving Robot Policy]] — 最终形成的优化循环

## 来源

- [[05_Papers/articles/rise|RISE: Self-Improving Robot Policy with Compositional World Model]]，第 III-A 节
