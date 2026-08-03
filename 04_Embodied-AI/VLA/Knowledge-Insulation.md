---
title: Knowledge Insulation
description: 在 VLA 训练中用 stop gradient 隔离动作专家，使其不影响模型其余部分的知识表示
tags:
  - embodied-ai
  - vla
  - training
  - concept
created: 2026-07-28
---

# Knowledge Insulation

VLA 训练方法，让模型同时学习离散 token（子任务文本、离散化动作 token）和连续动作（通过 [[Flow-Matching]]），并通过 stop gradient 防止动作专家反向传播影响 VLM 表示。

## Core Idea

在大规模预训练中：
- VLM 部分处理视觉-语言理解。
- 动作专家（action expert）基于 VLM 的激活生成连续动作。
- **stop gradient**：动作专家的梯度不回流到 VLM，避免动作生成任务“污染”视觉-语言知识。

## Training Objective

联合优化：
- 子任务文本 $\hat{\ell}$ 的自回归似然；
- 离散动作 token $a_{t:t+H}^\ell$ 的自回归似然；
- 连续动作块 $\mathbf{a}_{t:t+H}$ 的流匹配损失。

总对数似然可分解为：

$$
\log \pi_\theta(\mathbf{a}_{t:t+H}, a_{t:t+H}^\ell, \hat{\ell} | \mathbf{o}_t, \ell) = \log \pi_\theta(\hat{\ell}|\mathbf{o}_t, \ell) + \log \pi_\theta(a_{t:t+H}^\ell|\mathbf{o}_t, \ell, \hat{\ell}) + \log \pi_\theta(\mathbf{a}_{t:t+H}|\mathbf{o}_t, \ell, \hat{\ell})
$$

## Benefits

- 保护预训练的 VLM 知识不被动作分布变化破坏。
- 允许动作专家独立快速迭代。
- 支持多模态输出（文本 + 离散动作 + 连续动作）端到端训练。

## Application

- 用于 $\pi_{0.5}$、$\pi_{0.6}$ 等 flow-matching VLA 的预训练。
- 在 [[RECAP]] 中，$\pi_{0.6}^*$ 继承 KI 架构并加入优势条件输入。

## Related Concepts

- [[Vision-Language-Action-Model]] — KI 应用的对象
- [[Flow-Matching]] — 动作专家使用的连续动作生成方法
- [[RECAP]] — 在 KI 架构上增加优势条件进行 RL 训练
- [[Action-Tokenization|Action Tokenization]] / FAST — VLM backbone 的离散监督来源之一

## 补充：来自 [[04_Embodied-AI/VLA/Knowledge-Insulation|knowledge-insulation（已合并）]]

### 为什么有效

- 视觉-语言预训练知识容易被动作回归的高方差梯度破坏
- 离散任务（语言、FAST token）提供更稳定的监督信号
- Action expert 可以专注于动作多模态分布的学习，而不干扰通用表示

### 优缺点

- **优点**：稳定训练、保留预训练 VLM 能力、提升泛化、允许独立设计动作专家
- **局限**：需要分别优化两个部分；action expert 可能无法充分利用 backbone 的细粒度更新

### 其他来源

- Danny Driess et al., *Knowledge Insulating Vision-Language-Action Models: Train Fast, Run Fast, Generalize Better*, NeurIPS 2025
- [[05_Papers/articles/pi0-7|π0.7]]，第 III、VI-B 节
