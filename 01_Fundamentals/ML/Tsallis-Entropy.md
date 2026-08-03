---
title: "Tsallis Entropy"
description: "Tsallis q-熵：从 Boltzmann-Gibbs 熵推广到非广延统计力学的广义信息度量"
tags: [concept, ml, information-theory, entropy, tsallis]
created: 2026-08-03
---

# Tsallis Entropy

Tsallis 熵是经典 Shannon 熵的单参数推广族，通过参数 $q$ 控制对稀有事件的敏感度。

## 定义

Tsallis $q$-对数：

$$
\log_q(u) = \frac{u^{1-q} - 1}{1-q}, \quad 0 < u \leq 1
$$

- $q \to 1$ 时 $\log_q(u) \to \ln(u)$，退化为标准对数
- $q = 0$ 时 $\log_0(u) = u - 1$，线性行为
- $q > 1$ 时重视大概率事件（mode-seeking）；$q < 1$ 时重视小概率事件（tail-seeking）

## 在机器学习中的应用

### 损失函数设计

用 $\log_q$ 替代标准损失中的 $\log$，构造 $q$-损失族：

$$J_Q(\theta, q) = \mathbb{E}[-\log_q(P_\theta)]$$

- **$q=0$**: exploitation pole，等价于期望损失（如 RLVR），有界 $[0,1]$
- **$q=1$**: density-estimation pole，等价于对数似然（如 SFT），无界

### 推理模型训练

$q$ 控制模型对监督信号的"承诺速度"(commitment speed)：
- 高 $q$：梯度放大因子 $P_\theta^{-q}$，冷启动逃逸快，但易记忆噪声
- 低 $q$：梯度平缓，鲁棒过滤噪声，但逃逸速度受限于 $\Omega(1/p_0)$

## 相关概念

- [[01_Fundamentals/ML/Cold-Start-in-RL|Cold-Start in RL]] — 冷启动问题的形式化分析
- [[01_Fundamentals/ML/Focal-Loss|Focal Loss]] — 类似的难易样本加权机制

## 来源

- [[05_Papers/notes/tsallis-loss-continuum|Tsallis Loss Continuum]] — Tsallis 熵在推理模型训练中的应用
