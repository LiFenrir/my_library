---
title: "VLA Inference"
description: "VLA 模型在推理阶段的延迟特征与调度策略入口"
tags:
  - ai-infra
  - vla
  - inference
  - latency
  - scheduling
  - concept
  - edge-ai
created: 2026-07-28
---

# VLA Inference

VLA（Vision-Language-Action）模型的推理不仅涉及语言解码，还涉及视觉编码、多模态 pre-fill 和 action token 生成。其延迟特性与纯文本 LLM 有显著差异。

## 延迟分解

对于输出 $n$ 个 token 的查询，总延迟可写为：

$$
L(n) = P(I_t, x_t, m_t) + \sum_{i=1}^{n} D_i
$$

- $P(\cdot)$：多模态 pre-fill 成本，包含图像编码、投影、prompt 打包
- $D_i$：第 $i$ 个解码 token 的成本

## 关键指标

- **Time-To-First-Action (TTFA)**：从查询开始到第一个动作 token 可用的时间
- **Action Rate**：1000 / TTFA (Hz)
- **Pre-fill Fraction**：$\rho = P / T_{\mathrm{act}}$，表示 pre-fill 占总动作延迟的比例

## Pre-fill 主导 regime

在 compact edge 模型上，生成首 token 前的多模态 pre-fill 是主要瓶颈。典型测量：

- $P \approx 47.8$ ms
- 每个解码 token 约 1.4 ms
- $\rho \approx 0.944$

这意味着：

- 缩短输出 token 数量对 TTFA 改善有限
- 优化 pre-fill 路径（减少视觉 token、缓存 prompt 结构、重叠预处理）更有价值

## 关键概念

- **Pre-fill Dominance**：多模态 pre-fill 是主要瓶颈
- **Time-to-First-Action (TTFA)**：从查询到第一个有效 action token 的延迟，是机器人反应能力的核心指标
- **Dual-Rate Scheduling**：将高速动作分支与低速语义分支分离，避免语义生成拖累动作 deadline
- **Edge Runtime Tradeoffs**：FP16、截断上下文、视觉 token 数量等都会影响边缘部署性能

## 与机器人控制的关系

反应延迟不仅取决于模型吞吐，还取决于 time-to-first-action 和动作执行 horizon。因此：

- 不能只报告平均 throughput
- 需要区分首次动作延迟和完整语义解码延迟
- 动作分支应 deadline-critical，语义分支可 opportunistic

## Related Concepts

- [[04_Embodied-AI/VLA/Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 基于延迟分解的调度策略
- [[04_Embodied-AI/VLA/Real-time-Action-Chunking|Real-Time Action Chunking]] — 处理推理延迟的动作生成技术
- [[04_Embodied-AI/VLA/Edge-VLA-Inference|Edge VLA Inference]] — 边缘部署延迟分析
- [[02_AI/AI-Infra/index|AI Infra]] — 模型服务与推理优化基础设施

## Papers

- [[05_Papers/notes/litevla-h|LiteVLA-H]] — 双速率 VLA 推理
- [[05_Papers/notes/litevla-edge|LiteVLA-Edge]] — 边缘量化 VLA
