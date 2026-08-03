---
title: Offline Reinforcement Learning
description: 从固定离线数据集中学习策略，无需与环境在线交互的强化学习范式
tags:
  - reinforcement-learning
  - offline-rl
  - concept
created: 2026-07-28
---

# Offline Reinforcement Learning

从预先收集的固定数据集 $\mathcal{D}$ 中学习策略，训练过程中不再与环境交互。

## Why It Matters

- 真实机器人、医疗、推荐系统等场景在线采样昂贵或危险。
- 可利用大规模历史演示数据（如人类遥操作、先前策略 rollout）。

## Core Challenge: Distribution Shift

学习策略可能访问数据分布外的状态-动作对，导致值函数外推错误（bootstrapping error）。

常见缓解手段：
- [[Regularized-RL]]：约束策略靠近 behavior policy。
- 悲观值估计：降低分布外样本的值。
- 模型集成或不确定度估计。

## Representative Methods

- **AWR / CRR**：优势加权回归，用监督学习拟合加权动作。
- **CQL**：通过正则化降低分布外 Q 值。
- **IQL**：隐式 Q 学习，避免显式查询学习策略的动作值。
- **Advantage-Conditioned**：将优势作为条件输入进行监督学习。
- **MOPO / MOReL**：模型化方法，学习世界模型并惩罚不确定性高的区域。

## 与 Imitation Learning 的区别

- 模仿学习假设数据是专家演示，目标是复现行为
- Offline RL 可以处理次优、异构数据，目标是从数据中提取比行为策略更好的策略

## Application to Robotics

- 用人类演示预训练通用策略。
- 将自主 rollout、专家干预等异构数据统一纳入训练，如 [[RECAP]]。
- 在视觉-语言-动作（VLA）策略 refinement 中，环境奖励通常不可得。可用学习得到的奖励模型（如 [[Advantage-Reward-Modeling|ARM]]）提供优势信号，实现无需在线交互的策略改进。

## Offline RL in Imitation Learning

当奖励函数不可得时，机器人领域常出现以下离线 RL 变体：

- **RA-BC**（Reward-Aligned Behavior Cloning）：用子任务级奖励模型对样本加权；
- **AW-BC**（Advantage-Weighted Behavior Cloning）：用 ARM 估计的相对优势 $\Delta G_t$ 对行为克隆样本加权，可处理碎片化、异构的 DAgger 数据。

两者都可视为离线 RL 在机器人模仿学习中的实例化：在约束策略靠近行为策略的同时，最大化加权动作似然。

## Related Concepts

- [[Regularized-RL]] — 稳定离线训练的核心技术
- [[Policy-Extraction]] — 从值函数导出策略
- [[Offline-RL-for-VLA]] — 面向 VLA 的离线 RL 实践
- [[RECAP]] — 迭代离线 RL 训练 VLA 的方法
- [[Imitation-Learning]] — 行为克隆基础范式
- [[Advantage-Reward-Modeling]] — 无需环境奖励的优势估计
- [[Advantage-Weighted-Behavior-Cloning]] — 机器人场景下的优势加权 BC
- [[Long-Horizon-Manipulation-Reward]] — 长程操作奖励设计问题

## 来源

- [[05_Papers/articles/pi-0-6|π*0.6: A VLA That Learns From Experience]]，第 I、II 节
