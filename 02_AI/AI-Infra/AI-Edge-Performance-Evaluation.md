---
title: AI Edge Performance Evaluation
description: 面向边缘 AI 工作负载的混合评测方法：真实硬件剖析 + 高保真模拟器投影
tags:
  - ai-infra
  - evaluation
  - edge-inference
  - benchmarking
  - performance-model
created: 2026-07-28
---

# AI Edge Performance Evaluation

评估边缘 AI 工作负载（如 VLA）时，单一真实硬件测试无法覆盖未来模型与硬件。可采用**实测 + 高保真模拟**的混合方法。

## 方法框架

```
真实硬件剖析  →  基线延迟与瓶颈分解
      ↓
模拟器投影    →  未来模型/硬件配置的性能预测
```

## 真实硬件剖析

- **平台示例**：NVIDIA Jetson AGX Orin（64GB LPDDR5）、Jetson Thor（128GB LPDDR5X）。
- **工具**：NVIDIA Nsight Compute 等内核级性能分析工具。
- **输出**：将端到端延迟分解为视觉编码、自回归解码、动作生成等阶段。
- **作用**：建立经验基线，识别实际运行时的内存/计算瓶颈。

## 高保真模拟器投影

用于评估更大模型（如 10B–100B）与假设硬件配置。

### 核心能力

- **微架构保真**：建模 SMs 数量、tiling 策略、矩阵引擎各维度的不对称带宽。
- **解析式 Roofline**：对每个算子同时考虑算力与内存带宽约束。
- **跨算子优化**：建模操作符边界的有效预取，减少内存层级停顿。

### 模型分解

将 VLA 拆分为多层 Transformer backbone，每层再分解为以高维 einsum 为主的算子序列，分别建模：

1. Vision Encoding
2. Autoregressive Decoding
3. Action Generation

### 精度

对生产级加速器（GPU、TPU）的验证显示，模拟器对若干生产模型的预测精度约为 **70%–90%**。

## 关键指标

- **端到端延迟 / 单步延迟**
- **控制频率（Control Frequency）**：动作更新频率，机器人通常要求 10–20 Hz。
- **阶段延迟占比**：定位瓶颈阶段。
- **内存带宽利用率**：判断是否为内存受限 workload。

## Related Concepts

- [[Roofline-Model|Roofline Model]] — 算力-带宽联合约束的性能模型
- [[VLA-Edge-Characterization|VLA Edge Characterization]] — 本方法在 VLA 上的应用实例
- [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘 VLA 的延迟分解与 TTFA

## Papers

- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 本笔记主要知识来源
