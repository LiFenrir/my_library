---
title: "Variational Autoencoder"
description: "通过引入隐变量先验与重参数化技巧学习数据低维潜在表示的生成模型。"
tags: [concept, ml, generative-model, vae, latent-variable-model]
created: 2026-07-28
---

# Variational Autoencoder

变分自编码器（VAE）是一种生成模型，通过编码器-解码器结构学习数据的低维潜在表示，并对潜在变量施加先验分布，使潜在空间具有良好结构。

## 核心思想

- 观测 $x$ 由未观测的连续潜在变量 $z$ 生成。
- 编码器输出潜在分布参数 $\mu, \sigma$。
- 从中采样 $z \sim \mathcal{N}(\mu, \sigma I)$，经解码器重建 $x$。
- 优化证据下界（ELBO），同时约束重建误差与 KL 散度。

## 训练目标

$$
\mathcal{L}(\theta, \phi; x) = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x) \| p(z))
$$

- 重建项：输入与解码输出的相似度。
- KL 项：后验 $q_\phi(z|x)$ 与先验 $p(z)$（通常为标准高斯）的接近程度。

## 在 World Model 中的角色

在 [[World-Model|World Model]] 的 V 模块中，VAE 把高维像素帧压缩为低维 $z$，让动力学模型 M 在潜在空间而非像素空间预测未来。

## 优缺点

- 优点：可学习压缩、结构化潜在空间；支持生成与插值。
- 局限：重建可能丢失任务相关细节；KL 约束限制信息容量；对复杂图像生成质量通常不如扩散模型。

## 相关概念

- [[Mixture-Density-Network|MDN]] — 用于建模多模态条件分布的输出层。
- [[World-Model]] — 将 VAE 作为感知压缩模块的应用场景。

## 来源

- [[05_Papers/articles/world-models|World Models]]
