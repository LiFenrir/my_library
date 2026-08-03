---
title: VLA Inference
description: VLA 模型在推理阶段的延迟特征与调度策略入口
tags:
  - ai-infra
  - vla
  - inference
  - latency
  - scheduling
created: 2026-07-28
---

# VLA Inference

VLA（Vision-Language-Action）模型的推理不仅涉及语言解码，还涉及视觉编码、多模态 pre-fill 和 action token 生成。其延迟特性与纯文本 LLM 有显著差异。

## 关键概念

- **Pre-fill Dominance**：在 compact edge 模型上，生成首 token 前的多模态 pre-fill 是主要瓶颈。
- **Time-to-First-Action (TTFA)**：从查询到第一个有效 action token 的延迟，是机器人反应能力的核心指标。
- **Dual-Rate Scheduling**：将高速动作分支与低速语义分支分离，避免语义生成拖累动作 deadline。
- **Edge Runtime Tradeoffs**：FP16、截断上下文、视觉 token 数量等都会影响边缘部署性能。

## 详细笔记

- [[Edge-VLA-Inference|Edge VLA Inference]] — 延迟分解、pre-fill dominance、优化方向
- [[Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 双速率调度策略
- [[Outer-Loop-Guidance|Outer-Loop Guidance]] — VLA 作为控制外环的分层设计
- [[Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — 专业化训练与知识保持

## Papers

- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 本笔记主要知识来源
