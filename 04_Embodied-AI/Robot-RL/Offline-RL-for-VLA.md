---
title: Offline RL for VLA
description: 将离线强化学习应用于 Vision-Language-Action 模型的训练范式
tags:
  - embodied-ai
  - robot-rl
  - vla
  - offline-rl
  - concept
created: 2026-07-28
---

# Offline RL for VLA

在不依赖持续在线交互的情况下，用历史数据（演示、自主 rollout、专家干预）训练或改进 Vision-Language-Action（VLA）模型。

## Why Needed

- VLA 通常先在大量人类演示上预训练，但 imitation learning 存在复合误差，且无法超越演示水平。
- 真实机器人部署中，在线策略梯度训练成本高、不稳定。
- 离线 RL 允许将部署中收集的失败与成功经验统一复用。

## Key Challenges

- **异构数据**：不同来源（人、旧策略、新策略）的动作分布不同。
- **分布偏移**：学习策略可能访问数据分布外状态。
- **大模型稳定性**：VLA 参数量大，传统 PPO 难以稳定训练。

## Typical Pipeline

1. **预训练**：在大型多任务演示数据集上同时训练 VLA 和值函数（offline RL）。
2. **任务特化**：用目标任务的演示进行 SFT，固定优势指示器为 positive。
3. **迭代改进**：
   - 部署策略收集自主经验；
   - 专家 optionally 干预纠正；
   - 用全部数据重新训练值函数；
   - 用更新的优势估计重新训练 VLA。

## Methods

- **AWR / CRR**：优势加权回归，但会丢弃大量数据。
- **PPO / REINFORCE**：需要 on-policy 数据，难以扩展到大 VLA。
- **Advantage Conditioning**：RECAP 采用的方法，监督学习目标、适配流匹配 VLA。

## Related Concepts

- [[RECAP]] — 面向 VLA 的迭代离线 RL 方法
- [[Advantage-Conditioning]] — RECAP 使用的策略提取技术
- [[Offline-Reinforcement-Learning]] — 通用离线 RL 基础
- [[[[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]] — 离线 RL 的模型对象
