---
title: "Tsallis Loss Continuum"
description: "用 Tsallis q-对数统一 RLVR 中的损失函数，在冷启动信号放大与训练稳定性之间连续调节"
tags: [concept, ml, rlvr, reasoning, tsallis]
created: 2026-07-30
---

# Tsallis Loss Continuum

**核心定义**：Tsallis Loss Continuum 是一类基于 Tsallis $q$-对数的损失函数族，用于带隐式推理轨迹的强化学习（RLVR），通过参数 $q$ 在连续谱上调节梯度特性，平衡冷启动信号放大与训练稳定性。

## 背景问题

在 RLVR 中，模型生成隐式推理链 $z$ 后再输出答案 $y$。仅有输出级监督时：

- 冷启动阶段模型几乎无法得到非零奖励，梯度稀疏；
- Rao-Blackwellized 奖励虽能保证非零梯度，但仅降低方差，不解决逃离低密度区速度；
- 高 $q$ 放大低概率轨迹信号，但可能导致训练崩溃。

## Tsallis $q$-对数

Tsallis $q$-对数定义为：

$$
\log_q(x) = \frac{x^{1-q} - 1}{1 - q}
$$

当 $q \to 1$ 时退化为标准对数；$q < 1$ 时放大低概率区域的梯度信号。

## 两个具体算法

### 1. GARL（Gradient-Amplified Reinforcement Learning）

直接在目标中引入 $q$-对数，放大成功概率较低时的梯度：

- **优点**：冷启动信号强，逃离低密度区快；
- **缺点**：高 $q$ 下容易崩溃（collapse to zero）。

### 2. PAFT（Posterior-Adjusted Fine-Tuning）

用 $q$-对数加权后验采样，降低方差并提高稳定性：

- **优点**：在 $q \geq 0.75$ 时不易崩溃；
- **缺点**：每步信号较弱。

## 选择策略

- **冷启动**：使用 GARL（低 $q$ 或稳定任务）；
- **高 $q$ / 复杂任务**：使用 PAFT 避免崩溃；
- 实际决策常归结为「稳定 vs 不稳定」而非简单高 $q$ vs 低 $q$。

## 与其他概念的关系

- [[01_Fundamentals/ML/Regularized-RL|Regularized RL]] — 同属损失/梯度正则化方法
- [[02_AI/LLM/Chain-of-Thought-Reasoning|Chain-of-Thought Reasoning]] — 隐式推理轨迹的应用场景
- [[01_Fundamentals/ML/Credit-Assignment|Credit Assignment]] — RLVR 中的核心挑战

## 来源

- [[05_Papers/articles/tsallis-loss-continuum|Tsallis Loss Continuum]]
