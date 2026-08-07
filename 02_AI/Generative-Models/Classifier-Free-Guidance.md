---
title: Classifier-Free Guidance
description: 通过对比条件生成与无条件生成来增强条件生成模型可控性的技术
tags:
  - ai
  - concept
  - generative-model
  - diffusion
  - flow-matching
  - conditioning
created: 2026-07-28
---

# Classifier-Free Guidance

Classifier-Free Guidance（CFG）是一种**条件生成模型**的引导技术，通过放大条件信号对生成结果的影响来提升样本质量和条件遵循度。

## Core Idea

在训练时随机丢弃条件信息，使模型同时学会条件生成和无条件生成。在推理时，将条件生成方向与无条件生成方向的差值叠加到条件生成结果上：

$$
\nabla_a \log p(a \mid c) + \beta \left( \nabla_a \log p(a \mid c) - \nabla_a \log p(a) \right)
$$

其中 $\beta$ 为引导权重，控制条件遵循强度。

## 原理（扩散模型形式化）

设条件生成模型为 $\epsilon_\theta(\mathbf{x}_t, t, c)$，无条件版本为 $\epsilon_\theta(\mathbf{x}_t, t, \emptyset)$。CFG 在推理时的修正输出为：

$$
\hat{\epsilon} = \epsilon_\theta(\mathbf{x}_t, t, \emptyset) + \beta \left( \epsilon_\theta(\mathbf{x}_t, t, c) - \epsilon_\theta(\mathbf{x}_t, t, \emptyset) \right)
$$

$\beta = 1$ 为普通条件采样；$\beta > 1$ 增强条件对齐，但可能降低多样性。

## 训练方式

- 训练时以概率 $p$（通常 0.1~0.15）将条件 $c$ 替换为空条件 $\emptyset$
- 同一次前向传播同时学习两种模式
- 无需额外训练分类器，避免了分类器梯度估计的困难

## Why It Works

- 避免额外训练分类器
- 通过调整 $\beta$ 在样本多样性与条件忠实度之间权衡
- 可应用于文本、图像、动作等多种条件

## Key Parameters

- **Dropout rate**：训练中条件丢弃比例
- **Guidance weight $\beta$**：推理时的引导强度，常用值 1.3–2.2

## 优缺点

- **优点**：实现简单、无需外部分类器、可灵活调节 guidance scale、广泛应用于扩散/流模型
- **局限**：过高的 $\beta$ 会导致样本多样性下降、分布外行为或模式坍缩

## In Robotics

CFG 可用于引导 VLA 的动作生成朝向特定提示条件。在 π0.7 中，CFG 被用于 episode metadata、subtask instruction 等条件的推理增强。例如，通过设置较高的 speed/quality metadata，引导策略产生更快、更高质量的动作；公式形式为：

$$
\nabla_{\mathbf{a}} \log \pi_\theta(\mathbf{a}_{t:t+H} | \mathbf{o}_t, \mathcal{C}_t) + \beta \left( \nabla_{\mathbf{a}} \log \pi_\theta(\mathbf{a}_{t:t+H} | \mathbf{o}_t, \mathcal{C}_t) - \nabla_{\mathbf{a}} \log \pi_\theta(\mathbf{a}_{t:t+H} | \mathbf{o}_t, \mathcal{C}_t^{\text{uncond}}) \right)
$$

## Related Concepts

- [[02_AI/Generative-Models/Flow-Matching|Flow Matchin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — CFG 可与其结合用于动作去噪
- [[04_Embodied-AI/VLA/Diverse-Prompting-for-VLA|Diverse Prompting for VL[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — 在 VLA 中对多种提示组件应用 CFG
- [[01_Fundamentals/ML/diffusion-model|Diffusion Mode[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — CFG 最初提出于扩散模型
- [[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]]|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — π0.7 中对 metadata 使用 CFG 强化控制

## Papers

- [[05_Papers/articles/pi0-7|π0.[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — 对 episode metadata 应用 CFG 以提升灵巧任务性能（第 VII 节）
- Jonathan Ho & Tim Salimans, *Classifier-Free Diffusion Guidance*, arXiv:2207.12598
