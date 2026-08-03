---
title: Neural Scaling Laws
description: 模型性能随规模、数据、算力按幂律增长的实证规律
tags:
  - fundamentals
  - ml
  - scaling-law
  - large-model
  - concept
created: 2026-07-30
---

# Neural Scaling Laws

Neural Scaling Laws（神经缩放律）描述深度学习模型性能随**模型规模、数据量、计算量**增长而呈现的**幂律（power-law）**关系：当其中一个变量增加而其他变量充足时，测试损失或任务性能会按幂律改善。

## Core Idea

对大规模模型，常见观测形式为：

```
L(N) ∝ N^(-α)
L(D) ∝ D^(-β)
L(C) ∝ C^(-γ)
```

- `L`：测试损失或误差
- `N`：模型参数量
- `D`：训练 token 数
- `C`：训练计算量
- `α, β, γ`：正的幂律指数，通常小于 1

即在双对数坐标下，性能与规模呈线性关系。

## Why It Matters

缩放律提供了一种预测性框架：

- **规划训练资源**：给定目标性能，可反推所需参数、数据与算力。
- **指导模型设计**：在数据充足时，扩大模型规模通常比复杂架构改动更有效。
- **跨领域迁移**：缩放律在语言、视觉、多模态乃至机器人任务中均有观测。

## In Robotics

在具身智能与机器人控制中，缩放律表现为：

- 机器人任务性能随模型规模按幂律提升。
- 要达到复杂真实环境的通用能力，VLA 等模型规模可能需要达到 **10–100B 参数**量级。
- 但规模增长也带来边缘部署的实时性与内存带宽挑战。

## Limitations

- **数据质量**：缩放律假设数据充分且分布稳定；低质量或分布外数据会打破规律。
- **推理成本**：训练侧缩放与推理侧效率需同时考虑。
- **任务饱和**：某些简单任务可能在较小规模即达到性能平台。
- **可解释性**：缩放律是经验规律，不揭示模型内部机制。

## Related Concepts

- [[VLA-Edge-Characterization|VLA Edge Characterization]] — 缩放律驱动的 VLA 规模与边缘延迟冲突
- [[Edge-VLA-Inference|Edge VLA Inference]] — 规模增长对边缘推理的影响
- [[Mixture-of-Experts|Mixture of Experts]] — 通过稀疏激活在扩大参数的同时控制推理成本

## Papers

- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 引用神经缩放律作为 VLA 规模化的动机
