---
title: "Diffusion Model"
description: "通过逐步去噪学习数据分布的生成模型家族，包含 score matching、EDM、latent diffusion 与 diffusion transformer 等核心变体"
tags: [concept, ml, generative-model, diffusion-model, score-matching]
created: 2026-07-30
---

# Diffusion Model

**核心定义**：Diffusion Model 是一类生成模型，通过向数据逐步加入噪声再学习逆向去噪过程来建模复杂数据分布。

## 核心思想

1. **前向过程**：给干净样本 $\mathbf{x}_0$ 逐步添加高斯噪声，得到噪声水平递增的序列 $\mathbf{x}_1, \ldots, \mathbf{x}_T$。
2. **逆向过程**：训练神经网络预测噪声或干净样本，从纯噪声逐步恢复数据。
3. **Score Matching**：去噪网络本质上学习的是数据分布的对数梯度（score function）$\nabla_{\mathbf{x}} \log p(\mathbf{x})$。

## EDM 去噪目标

Karras et al. (2022) 提出的 EDM（Elucidating the Design Space of Diffusion Models）框架将训练目标统一为对去噪器 $D_\theta$ 的回归：

$$
\mathcal{L}(D_\theta, \sigma) = \mathbb{E}_{\mathbf{x}_0, \mathbf{c}, \mathbf{n}} \left[ \| D_\theta(\mathbf{x}_0 + \mathbf{n}; \sigma, \mathbf{c}) - \mathbf{x}_0 \|_2^2 \right]
$$

其中：
- $\mathbf{x}_0$：干净样本（如 VAE 编码后的潜在序列）
- $\mathbf{c}$：条件信息（如文本 embedding）
- $\sigma$：噪声水平
- $\mathbf{n} \sim \mathcal{N}(\mathbf{0}, \sigma^2 \bar{\mathbf{I}})$：与 $\mathbf{x}_0$ 同形的高斯噪声
- $D_\theta$：去噪网络，通常通过 cross-attention 条件化 $\mathbf{c}$，通过 adaptive layer normalization 条件化 $\sigma$

## 关键变体

| 变体 | 核心特点 |
|------|----------|
| **DDPM** | 离散时间步扩散，直接预测噪声 |
| **EDM** | 连续噪声水平，统一设计空间 |
| **Latent Diffusion** | 在 VAE 压缩的潜在空间进行扩散，降低计算成本 |
| **Diffusion Transformer (DiT)** | 用 Transformer 替代 U-Net 作为去噪 backbone |
| **Flow Matching** | 直接学习常微分连续概率路径，可视为扩散的连续极限 |

## 在机器人中的应用

- **Diffusion Policy**：将动作生成视为去噪回归，建模多峰动作分布
- **Video-based Robot Policy**：在视频扩散模型的潜在空间中生成动作、未来状态和价值
- **World Model**：通过视频扩散模型学习环境动力学

## 优缺点

- **优点**：可建模复杂多峰分布；有成熟的条件化与引导技术（如 [[02_AI/Generative-Models/Classifier-Free-Guidance|Classifier-Free Guidance]]）；可利用大规模无标注数据预训练
- **缺点/局限**：采样需要多步迭代，推理慢；对噪声 schedule 敏感；长程一致性仍具挑战

## 与其他概念的关系

- [[02_AI/Generative-Models/Flow-Matching|Flow Matching]] — 与扩散模型关系密切的连续生成框架
- [[02_AI/Generative-Models/Classifier-Free-Guidance|Classifier-Free Guidance]] — 扩散模型条件生成的常用技术
- [[04_Embodied-AI/World-Model/latent-frame-injection|Latent Frame Injection]] — 在潜在扩散序列中注入新模态的机器人策略方法
- [[04_Embodied-AI/World-Model/video-foundation-model-for-robotics|Video Foundation Model for Robotics]] — 视频扩散模型在机器人中的具体应用

## 来源

- [[05_Papers/articles/cosmos-policy|COSMOS POLICY: Fine-Tuning Video Models for Visuomotor Control and Planning]]，第 3 节
- Karras et al., "Elucidating the Design Space of Diffusion-Based Generative Models", NeurIPS 2022
- Peebles & Xie, "Scalable Diffusion Models with Transformers", ICCV 2023
