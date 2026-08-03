---
title: "LLM/VLA 推理延迟分解"
description: "将多模态模型推理延迟拆分为预填充与逐 token 解码两阶段，并指出边缘短输出场景常为预填充主导。"
tags: [concept, ai-infra, inference, vla, latency]
created: 2026-07-28
---

# LLM/VLA 推理延迟分解

核心定义：一次自回归推理的总延迟可拆分为处理输入的预填充（pre-fill）阶段与逐个生成输出 token 的解码阶段。

## 公式

$$
L(n) = P(I_t, x_t, m_t) + \sum_{i=1}^{n} D_i
$$

- $P(\cdot)$：多模态预填充延迟，包含视觉编码、投影、提示打包等。
- $D_i$：第 $i$ 个输出 token 的解码延迟。
- $n$：输出 token 数量。

## 关键观察

- 在紧凑模型与短动作输出的边缘场景下，通常满足 $P \gg D_i$（预填充主导）。
- 此时优化输出长度对首 token 延迟影响有限，首要优化方向是降低预填充成本。
- 常用指标：time-to-first-action（TTFA，首动作延迟）。

## 来源

- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 在 Jetson AGX Orin 上测得预填充约占 94.4% 的动作查询延迟。
