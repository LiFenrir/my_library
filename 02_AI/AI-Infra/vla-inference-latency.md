---
title: "VLA Inference Latency"
description: "分析 VLA 部署中预填充、解码、上下文长度等因素对推理延迟影响的系统问题"
tags: [concept, ai-infra, vla, edge-ai]
created: 2026-07-29
---

# VLA Inference Latency

**核心定义**：VLA Inference Latency 关注将 VLA 部署到真实机器人系统时的端到端推理时间，包括多模态预填充（pre-fill）、token 解码、后处理和通信延迟。

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

在 LiteVLA-H 的测量中：

- $P \approx 47.8$ ms
- 每个解码 token 约 1.4 ms
- $\rho \approx 0.944$

这意味着：

- 缩短输出 token 数量对 TTFA 改善有限
- 优化 pre-fill 路径（减少视觉 token、缓存 prompt 结构、重叠预处理）更有价值

## 与机器人控制的关系

反应延迟不仅取决于模型吞吐，还取决于 time-to-first-action 和动作执行 horizon。因此：

- 不能只报告平均 throughput
- 需要区分首次动作延迟和完整语义解码延迟
- 动作分支应 deadline-critical，语义分支可 opportunistic

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 基于延迟分解的调度策略
- [[04_Embodied-AI/VLA/Real-time-Action-Chunking|Real-Time Action Chunking]] — 处理推理延迟的动作生成技术
- [[02_AI/AI-Infra/index|AI Infra]] — 模型服务与推理优化基础设施

## 来源

- [[05_Papers/articles/litevla-h|LiteVLA-H: Dual-Rate Vision-Language-Action Inference for Onboard Aerial Guidance and Semantic Perception]]，第 3.3、5.3、6.1、9.1 节
