---
title: "Learning to Think"
description: "Schmidhuber 提出的 RNN 控制器与世界模型协同的通用问题求解框架"
tags: [concept, ml, rl, world-model, controller, rnn, schmidhuber]
created: 2026-07-30
---

# Learning to Think

Learning to Think 是 Schmidhuber 于 2015 年提出的一个统一框架，旨在构建一个基于 RNN 的通用问题求解器：一个 RNN 控制器 $C$ 与一个 RNN 世界模型 $M$ 协同工作，$C$ 学会利用、忽略或改写 $M$ 的内部子程序来完成任务。

## 核心思想

- **C–M 分离**：控制器 $C$ 负责决策，世界模型 $M$ 负责对环境进行预测与模拟。
- **$C$ 可以调用 $M$ 的子程序**：$C$ 不必逐帧滚动未来，而是可以学习使用 $M$ 的权重矩阵片段作为可复用计算模块，实现分层规划、推理等任意可计算操作。
- **$C$ 可以忽略 $M$**：当 $M$ 的预测不可靠时，$C$ 可以选择不依赖它，从而避免被错误动力学误导。
- **可进化/可训练**：$C$ 既可以通过传统 RL 训练，也可以通过进化策略等黑箱优化方法训练。

## 与 World Models 的关系

[[World-Model|World Models]]（Ha & Schmidhuber, 2018）是 Learning to Think 的一个简化实验框架：

- 使用 [[Variational-Autoencoder|VAE]] 作为 $V$ 模块压缩感知输入。
- 使用 [[Mixture-Density-Network|MDN-RNN]] 作为 $M$ 模块学习潜在动力学。
- 使用极简线性控制器 $C$ 并通过 [[Evolution-Strategies|CMA-ES]] 优化。

与完整 Learning to Think 不同，World Models 中的 $C$ 更接近早期 C–M 系统，依赖 $M$ 逐帧预测未来，尚未充分利用 $M$ 的子程序能力。

## 扩展方向

- **One Big Net**：将 $C$ 与 $M$ 合并为单一网络，通过类似 PowerPlay 的行为回放压缩旧技能，避免灾难性遗忘。
- **PowerPlay / 课程学习**：自动寻找当前系统能解决的最简单未解决问题，形成自然课程，逐步扩展能力。
- **人工好奇心与内在动机**：让智能体主动探索能改善世界模型的区域，作为迭代训练的动力。

## 优缺点

- 优点：框架通用，允许 $C$ 灵活使用 $M$；可扩展至分层规划与抽象推理。
- 局限：早期 C–M 系统依赖 $M$ 的逐步预测，容易受模型误差累积影响；$C$ 学会如何利用 $M$ 本身是一个高难度优化问题。

## 相关概念

- [[World-Model]] — Learning to Think 的简化神经实现。
- [[Model-Based-Reinforcement-Learning|Model-Based RL]] — 学习环境动力学并用于决策的方法论。
- [[Mixture-Density-Network|MDN]] — 用于建模多模态未来的输出层。
- [[Evolution-Strategies|Evolution Strategies]] — 可用于优化 $C$ 的黑箱方法。

## 来源

- [[05_Papers/articles/world-models|World Models]]，Ha & Schmidhuber, 2018
