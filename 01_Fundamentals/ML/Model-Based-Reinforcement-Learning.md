---
title: "Model-Based Reinforcement Learning"
description: "先学习环境动力学模型，再利用模型进行规划或策略训练的强化学习方法。"
tags: [concept, ml, rl, model-based-rl, planning, world-model]
created: 2026-07-28
---

# Model-Based Reinforcement Learning

Model-Based RL（MBRL）先学习环境转移模型，再基于该模型做规划、生成虚拟经验或训练策略，以提升样本效率并支持长期推理。

## 与 Model-Free RL 的区别

- **Model-Free**：直接从经验中估计价值函数或策略，不对环境转移建模。
- **Model-Based**：显式学习 $P(s_{t+1}, r_{t+1} | s_t, a_t)$，用模型辅助决策。

## 核心组成

- **Dynamics Model / World Model**：预测下一状态与奖励。
- **Planning**：在模型中搜索最优动作序列（如 MPC、MCTS）。
- **Policy Training in Model**：在模型生成的 rollouts 上训练策略，再迁移到真实环境。

## 典型方法

- **PILCO**：使用高斯过程学习低维动力学，通过轨迹采样训练控制器。
- **Bayesian Neural Networks**：用贝叶斯网络建模不确定性。
- **Neural Network Simulators**：用 CNN/RNN 直接从像素学习前向模型。
- **Imagination-Augmented Agents**：在习得世界模型中想象未来以辅助决策。

## 与 World Model 的关系

[[World-Model|World Model]] 是 MBRL 的一种神经实现：VAE 压缩感知输入，RNN/MDN 学习潜在动力学，控制器在“梦境”中训练。

## 优缺点

- 优点：数据效率高；可廉价生成大量虚拟 rollouts；便于迁移与 Sim2Real。
- 局限：模型误差会累积（compounding error）；智能体可能利用模型缺陷；模型在分布外状态可能失效。

## 相关概念

- [[World-Model]] — 基于深度生成模型的世界模型实例。
- [[Evolution-Strategies]] — 可用于优化小控制器的优化方法。
- [[04_Embodied-AI/Sim2Real/index|Sim2Real]] — 利用仿真模型学到的策略迁移到真实环境。

## 补充：来自 [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]

LeCun 将自主智能体建模为模型预测控制（[[Model-Predictive-Control|MPC]]）的可学习版本：

- 世界模型不是显式转移概率 $P(s'|s,a)$，而是 [[Joint-Embedding-Predictive-Architecture|JEPA]] / [[Hierarchical-JEPA|H-JEPA]] 表示空间中的预测器。
- 成本模块 $C(s)$ 是可微的，由 Intrinsic Cost 与 Trainable Critic 组成，梯度可反向传播到动作。
- Actor 在 World Model 中展开未来轨迹，通过梯度优化动作序列。
- 与经典 MBRL 的区别：强调通过大量被动观察学习世界模型，而非仅靠环境奖励；奖励/成本只起相对次要作用。

## 来源

- [[05_Papers/articles/world-models|World Models]]
- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]，LeCun，2022
