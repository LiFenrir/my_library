---
title: Policy Extraction
description: 从已训练的值函数或优势函数中导出改进策略的过程
tags:
  - reinforcement-learning
  - offline-rl
  - policy-extraction
  - concept
created: 2026-07-28
---

# Policy Extraction

给定值函数或优势函数，学习一个新策略以利用这些估计，同时避免分布偏移和不稳定更新。

## Common Methods

| 方法 | 核心思想 | 适用场景 |
|------|---------|---------|
| 策略梯度 (PPO 等) | 沿优势方向更新策略参数 | 可精确计算似然的策略 |
| 加权回归 (AWR/CRR) | 用优势加权行为克隆目标 | 离线数据，连续动作 |
| 优势条件 (Advantage Conditioning) | 将优势作为输入条件进行监督学习 | 大模型、流匹配/扩散策略 |

## Challenge with Flow-Matching Policies

流匹配或扩散策略通常没有易处理的似然 $\\log \\pi_\\theta(\\mathbf{a}|\\mathbf{o})$，使得策略梯度方法难以直接应用。因此需要：

- 基于似然下界的 PPO 变体（如 FPO、DPPO）。
- 不需要似然的监督学习方法，如 [[Advantage-Conditioning]]。

## Advantage-Conditioned Extraction

基于 [[Regularized-RL]] 的 KL 约束最优解：

$$
\hat{\pi}(\mathbf{a}|\mathbf{o}, \ell) \propto \pi_{\mathrm{ref}}(\mathbf{a}|\mathbf{o}, \ell) \left( \frac{\pi_{\mathrm{ref}}(\mathbf{a}|I, \mathbf{o}, \ell)}{\pi_{\mathrm{ref}}(\mathbf{a}|\mathbf{o}, \ell)} \right)^\beta
$$

其中 $I$ 为二值化优势指示器。训练时同时学习条件与非条件分布，推理时通过 [[02_AI/Generative-Models/Classifier-Free-Guidance]] 组合。

## Related Concepts

- [[Regularized-RL]] — 策略提取的理论基础
- [[Advantage-Estimation]] — 提取所需的输入
- [[Advantage-Conditioning]] — 面向 VLA 的提取方法
- [[RECAP]] — 在 VLA 中实际应用优势条件提取
