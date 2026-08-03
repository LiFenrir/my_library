---
title: Roofline Model
description: 同时用算力峰值与内存带宽峰值界定算子性能上限的简化性能模型
tags:
  - fundamentals
  - performance-model
  - memory-bound
  - computer-architecture
created: 2026-07-28
---

# Roofline Model

Roofline Model 是一种快速判断算子性能瓶颈的简化模型：性能上限由**算力峰值**与**内存带宽峰值**共同决定。

## 核心思想

对任意算子，定义**运算强度（Operational Intensity）**：

```
运算强度 = 浮点运算次数 / 访问的字节数  (FLOPs/Byte)
```

然后：

- 若运算强度低 → 性能受限于**内存带宽**（Memory Bound）。
- 若运算强度高 → 性能受限于**峰值算力**（Compute Bound）。

## 在 AI 推理中的意义

- **稠密前向/编码**：通常运算强度高，接近 compute bound。
- **自回归解码 / 动作生成**：序列逐步扩展，访存频繁，通常运算强度低，落入 memory bound 区域。
- 因此，提升算力对 memory-bound 阶段收益有限；需要更高内存带宽或算法上减少访存。

## 与 VLA 的关联

在 VLA 边缘推理中：

- Vision Encoder 多为 compute bound。
- Generation（自回归解码）多为 memory bound。
- 当 Thor 的算力提升 5 倍而延迟仅提升 1.4 倍时，说明瓶颈在内存带宽而非算力。

## Related Concepts

- [[AI-Edge-Performance-Evaluation|AI Edge Performance Evaluation]] — 将 Roofline 用于边缘 AI 评测的方法
- [[VLA-Edge-Characterization|VLA Edge Characterization]] — 内存带宽瓶颈的实例分析
- [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘 VLA 的延迟特征

## Papers

- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 本笔记在 VLA 上下文的应用来源
