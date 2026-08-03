---
title: Joint Embedding Predictive Architecture
description: 在表示空间而非像素/ token 空间进行预测的非生成式世界模型架构
tags:
  - concept
  - ml
  - self-supervised-learning
  - joint-embedding
  - world-model
  - jepa
created: 2026-07-30
---

# Joint Embedding Predictive Architecture

Joint Embedding Predictive Architecture（JEPA）是一种非生成式架构，用于学习预测性世界模型。它不直接预测原始 $y$，而是预测 $y$ 的表示 $s_y$，从而让编码器自动剔除难以预测的无关细节。

## 核心结构

给定两个输入 $x$ 和 $y$（如视频的两个片段）：

1. 两个编码器分别提取表示：

$$
s_x = \operatorname{Enc}_x(x), \quad s_y = \operatorname{Enc}_y(y)
$$

2. 预测器根据 $s_x$ 与隐变量 $z$ 预测 $s_y$：

$$
\tilde{s}_y = \operatorname{Pred}(s_x, z)
$$

3. 能量为表示空间中的预测误差：

$$
E_w(x, y, z) = D(s_y, \operatorname{Pred}(s_x, z))
$$

4. 对隐变量取最小化：

$$
F_w(x, y) = \min_{z \in \mathcal{Z}} D(s_y, \operatorname{Pred}(s_x, z))
$$

## 表示多模态未来的两种方式

### 1. 编码器不变性

$y$ 编码器可对不可预测细节不变：多个不同的 $y$ 映射到同一个 $s_y$，从而共享低能量。

### 2. 隐变量 $z$

$z$ 捕获 $s_y$ 中无法从 $s_x$ 推断的信息。当 $z$ 在集合 $\mathcal{Z}$ 上变化时，预测器产生一族合理预测：

$$
\operatorname{Pred}(s_x, \mathcal{Z}) = \{ \tilde{s}_y = \operatorname{Pred}(s_x, z) \mid \forall z \in \mathcal{Z} \}
$$

## 非对比训练准则

JEPA 可用非对比方法训练，避免对比方法的维度灾难：

1. 最大化 $s_x$ 关于 $x$ 的信息量。
2. 最大化 $s_y$ 关于 $y$ 的信息量。
3. 使 $s_y$ 易从 $s_x$ 预测（最小化 $D(s_y, \tilde{s}_y)$）。
4. 最小化隐变量 $z$ 的信息量。

准则 1、2、4 共同防止能量崩塌。

## 隐变量正则化手段

为防止 $z$ 携带过多信息导致崩塌，可：

- 离散化 / 量化（如 VQ-VAE）。
- 低维 / 秩最小化。
- 稀疏化（$L_1$ 正则）。
- 随机化 / 加噪（如 VAE）。

## 相比生成模型的优势

- 不必预测每个像素或 token 的细节。
- 可忽略风中的树叶、水面波纹等不可预测细节。
- 更适合高维连续信号（如视频）的长期预测。

## 与其他概念的关系

- [[Energy-Based-Model|EBM]] — JEPA 是一种非生成式 EBM。
- [[Self-Supervised-Learning|SSL]] — JEPA 是 SSL 在世界模型中的具体架构。
- [[VICReg]] — 可用于实现 JEPA 非对比训练的信息最大化准则。
- [[Hierarchical-JEPA|H-JEPA]] — 将 JEPA 堆叠为分层世界模型。

## 来源

- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards Autonomous Machine Intelligence]]，LeCun，2022
