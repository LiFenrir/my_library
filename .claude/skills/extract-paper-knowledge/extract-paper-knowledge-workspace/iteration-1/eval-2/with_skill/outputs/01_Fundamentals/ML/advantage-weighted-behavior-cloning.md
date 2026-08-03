---
title: "优势加权行为克隆"
description: "利用优势估计对离线示范样本加权，抑制次优轨迹、放大高价值转移。"
tags: [concept, fundamentals, rl, offline-rl, behavior-cloning]
created: 2026-07-28
---

# 优势加权行为克隆

核心定义：给每个 (s, a) 样本赋予一个权重，权重反映该动作相对历史行为的优势，从而过滤低质量数据。

## 代表方法

- **AWR（Advantage-Weighted Regression）**：基于优势加权的离线策略改进。
- **AWAC**：结合 Actor-Critic 的优势加权离线 RL。
- **IQL（Implicit Q-Learning）**：隐式 Q 学习，避免需要在线交互。
- **RA-BC（Reward-Aligned Behavior Cloning）**：用阶段感知奖励模型替代环境奖励进行加权。
- **AW-BC（Advantage-Weighted Behavior Cloning）**：在 RA-BC 基础上用相对优势与长度自适应增益进行加权。

## 目标形式

一般可写为最大化加权对数似然：

$$
\max_\theta \mathbb{E}_{(s,a)\sim\mathcal{D}} \left[ \tilde{w}(s,a) \log \pi_\theta(a|s) \right]
$$

- $\tilde{w}(s,a)$：经裁剪和归一化后的优势权重。
- 负权重样本被抑制，高优势（如恢复行为）样本被优先学习。

## 优缺点

- 优点：无需在线交互即可从次优示范中提取改进策略。
- 局限：权重估计质量依赖奖励/优势模型；异常值可能主导训练。

## 来源

- [[05_Papers/articles/arm|ARM]]
