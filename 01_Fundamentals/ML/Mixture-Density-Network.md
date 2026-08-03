---
title: "Mixture Density Network"
description: "神经网络输出混合分布参数以建模多模态条件概率密度的方法。"
tags: [concept, ml, generative-model, mdn, density-estimation, multimodal]
created: 2026-07-28
---

# Mixture Density Network

混合密度网络（MDN）是一种把神经网络输出参数化为混合分布（常见为高斯混合）的方法，用于刻画条件分布的多模态与不确定性。

## 核心思想

传统回归网络输出单一点估计，难以表达“多种可能未来”。MDN 让网络输出混合权重 $\pi$、各分量均值 $\mu$、方差 $\sigma$（以及可选相关系数），从而建模：

$$
p(y|x) = \sum_{k=1}^{K} \pi_k(x) \, \mathcal{N}(y; \mu_k(x), \sigma_k(x))
$$

## 训练目标

最大化对数似然：

$$
\mathcal{L} = \sum_i \log \sum_{k=1}^{K} \pi_k(x_i) \, \mathcal{N}(y_i; \mu_k(x_i), \sigma_k(x_i))
$$

## MDN-RNN

当 MDN 作为循环网络输出层时，称为 MDN-RNN。它把时间信息引入混合分布，常用于序列生成与 [[World-Model|World Model]] 中的潜在动力学建模：

$$
P(z_{t+1} \mid a_t, z_t, h_t)
$$

## 优缺点

- 优点：能表达多模态未来；适合随机环境；采样时可调节温度 $\tau$ 控制多样性。
- 局限：分量数 K 是超参数；训练可能不稳定；单一高斯混合对高度复杂分布仍有局限。

## 相关概念

- [[Variational-Autoencoder|VAE]] — 提供低维潜在向量 $z$ 的压缩表示。
- [[World-Model]] — MDN-RNN 作为记忆/动力学模块的应用。

## 补充：来自 [[05_Papers/articles/world-models|World Models]]

在 World Models 的 MDN-RNN 中，混合高斯输出被用于建模潜在空间中的离散随机事件（例如怪物是否发射火球）。相比单一对角高斯，混合分布能更好刻画环境逻辑中的多模态分支。

### 温度参数与模式崩溃

采样时引入温度参数 $\tau$ 控制分布锐度：

- **低 $\tau$（如 0.1）**：分布接近确定性 LSTM，容易出现模式崩溃。在 VizDoom 实验中，低温度下怪物几乎不再发射火球，导致 $C$ 在梦境中得分极高，但迁移到真实环境后失败。
- **高 $\tau$**：增加梦境环境的不确定性，使 $C$ 更难利用模型缺陷，策略在真实环境中更鲁棒；但过高会让梦境过于困难，反而学不到有效策略。

因此，$\tau$ 不仅是采样多样性参数，也是**真实性与可剥削性之间的权衡**。

### 高斯混合 vs 单高斯

虽然 VAE 编码的每帧潜在向量 $z$ 本身是对角高斯，但帧与帧之间的转移可能包含离散分支（如敌人开枪/不开枪）。单一高斯难以在这些分支间跳转，而高斯混合的离散模式天然适合此类随机离散事件。

## 来源

- [[05_Papers/articles/world-models|World Models]]
