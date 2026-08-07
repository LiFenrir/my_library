---
title: Advantage Conditioning
description: 将动作的优势信息编码为策略输入条件，以监督学习方式提取改进策略
tags:
  - embodied-ai
  - robot-rl
  - vla
  - offline-rl
  - concept
created: 2026-07-28
---

# Advantage Conditioning

将动作的优势（advantage）转化为离散或连续的条件信号，喂给策略模型，使其学会在“好动作”与“坏动作”之间区分，从而从值函数中提取改进策略。

## Core Idea

对于参考策略 $\pi_{\mathrm{ref}}$，定义二值化改进指示器：

$$
I_t = \mathbb{1}\left(A^{\pi_{\mathrm{ref}}}(\mathbf{o}_t, \mathbf{a}_t, \ell) > \epsilon_\ell\right)
$$

训练时同时学习：
- 非条件策略 $\pi_\theta(\mathbf{a}_t | \mathbf{o}_t, \ell)$
- 条件策略 $\pi_\theta(\mathbf{a}_t | I_t, \mathbf{o}_t, \ell)$

目标函数为负对数似然：

$$
\min_\theta \mathbb{E}_{\mathcal{D}_{\pi_{\mathrm{ref}}}} \left[ -\log \pi_\theta(\mathbf{a}_t | \mathbf{o}_t, \ell) - \alpha \log \pi_\theta(\mathbf{a}_t | I_t, \mathbf{o}_t, \ell) \right]
$$

## Why Use It for VLA

- **规避似然困难**：流匹配/扩散 VLA 没有易处理的 $\log \pi_\theta(\mathbf{a}|\mathbf{o})$，策略梯度方法难以扩展。
- **利用离线数据**：可同时使用演示、旧策略 rollout、专家纠正等异构数据。
- **稳定**：监督学习目标，训练大模型更稳定。

## Relation to Regularized RL

基于 [[Regularized-RL]] 的 KL 约束最优解，改进策略可写成：

$$
\hat{\pi}(\mathbf{a}|\mathbf{o}, \ell) \propto \pi_{\mathrm{ref}}(\mathbf{a}|\mathbf{o}, \ell) \left( \frac{\pi_{\mathrm{ref}}(\mathbf{a}|I, \mathbf{o}, \ell)}{\pi_{\mathrm{ref}}(\mathbf{a}|\mathbf{o}, \ell)} \right)^\beta
$$

当 $\beta = 1$ 时，$\hat{\pi}$ 就是条件策略本身。

## Test-Time Sharpening

训练时随机 dropout $I_t$，使模型同时掌握条件与非条件分布。推理时可用 [[02_AI/Generative-Models/Classifier-Free-Guidance]] 组合两者，调节 $\beta$ 控制改进强度。

## 在 RISE 中的应用

RISE 通过 Policy Warm-up 将 Advantage Conditioning 注入 π0.5 VLA：

- 价值模型预测当前状态-动作块的优势；
- 策略将该优势作为上下文 token 输入；
- 高优势时生成更 decisive 的动作，低优势时生成保守/恢复动作。

## 补充：来自 [[04_Embodied-AI/Robot-RL/Advantage-Conditioning|advantage-conditioning（已合并）]]

优缺点：

- **优点**：无需策略梯度，训练稳定；适用于 flow matching/diffusion 等无显式似然的模型；可以利用离线和异构数据。
- **局限**：依赖价值函数质量；阈值 $\epsilon_\ell$ 需要按任务调整；过度优化可能导致分布外行为。

该机制同样应用于 π*0.6（RECAP），见 [[05_Papers/articles/pi-0-6|π*0.6: A VLA That Learns From Experience]] 第 IV-B 节。

## Related Concepts

- [[RECAP]] — 将优势条件用于 VLA 迭代训练的方法
- [[Policy-Extraction]] — 优势条件是一种策略提取方法
- [[Advantage-Estimation]] — 优势条件的输入
- [[02_AI/Generative-Models/Classifier-Free-Guidance]] — 推理时增强条件信号
- [[Regularized-RL]] — 优势条件的理论基础
- [[04_Embodied-AI/Robot-RL/policy-warm-up-for-world-model-rl|Policy Warm-up for World Model RL]] — 在 RISE 中注入优势条件
- [[04_Embodied-AI/World-Model/compositional-world-model|Compositional World Model]] — 提供价值模型和想象 rollout

## 来源

- [[05_Papers/articles/rise|RISE: Self-Improving Robot Policy with Compositional World Model]]，第 III-B 节
