---
title: Edge VLA Inference
description:  compact edge-deployed Vision-Language-Action model 的推理延迟特征与优化策略
tags:
  - embodied-ai
  - vla
  - edge-inference
  - latency
  - ai-infra
created: 2026-07-28
---

# Edge VLA Inference

在资源受限的嵌入式平台（如 NVIDIA Jetson AGX Orin）上部署 Vision-Language-Action（VLA）模型时，端到端延迟通常由**多模态 pre-fill** 主导，而非解码额外 token 的边际成本。

## 延迟分解

对于输出 n 个 token 的查询，总延迟可分解为：

```
L(n) = P(I_t, x_t, m_t) + Σ D_i
```

- `P`：多模态 pre-fill 成本（视觉编码 + 文本提示融合 + projector）
- `D_i`：第 i 个输出 token 的解码成本

在 compact edge  regime 中，对于短输出（如 1-2 个 action token）：

```
P >> D_i  for small n
```

这意味着系统是 **pre-fill dominant**。

## Time-to-First-Action (TTFA)

TTFA 是从模型查询开始到第一个有效 action token 可用的延迟。由于 pre-fill 占 action 查询延迟的绝大部分（例如 ~94%），**优化 TTFA 比缩短输出长度更重要**。

推论：
- 单纯把 one-token action 改成另一种 one-token 格式，不会显著改善反应时间。
- 必须优化 pre-fill 路径：减少视觉 token、简化 projector、缓存可复用提示结构等。

## Edge Runtime 权衡

- **模型规模**：compact backbone（如 256M）可在边缘芯片上稳定运行。
- **精度**：FP16 是内存占用与数值保真度的常用折中。
- **上下文长度**：截断上下文窗口（如 2048）以降低内存压力。
- **视觉 token 数量**：直接影响 pre-fill 成本，是首要优化点。

## 优化方向

按优先级：
1. 减少视觉 token 数量（如 visual token pruning）
2. 缓存可复用的提示结构
3. 简化 projector 计算
4. 将图像预处理与上一次控制执行重叠
5. 避免不必要的语义请求

## 与 Large Spatial-Reasoning VLA 的对比

本笔记聚焦于**紧凑边缘 VLA**（如 256M–7B），其端到端延迟是 **pre-fill dominant** 的。这与大尺度空间推理 VLA（如 10B–100B）不同：

- 紧凑模型：视觉编码与 projector 占主导，TTFA 是优化重点。
- 大模型：自回归动作生成阶段占主导（可达 ~75%），受限于内存带宽。

详见 [[VLA-Edge-Characterization|VLA Edge Characterization]]。

## Related Concepts

- [[Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 利用 pre-fill 主导特性，将动作与语义分支解耦到不同频率
- [[Outer-Loop-Guidance|Outer-Loop Guidance]] — VLA 作为外环引导，内环仍由高频率飞控/控制器负责
- [[Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — 在边缘模型专业化的同时保留通用多模态能力
- [[VLA-Architecture|VLA Architecture]] — VLA 的三阶段计算架构
- [[VLA-Edge-Characterization|VLA Edge Characterization]] — 大 VLA 在边缘硬件上的瓶颈与 scaling 分析
- [[02_AI/AI-Infra/AI-Edge-Performance-Evaluation|AI Edge Performance Evaluation]] — 边缘 AI 评测与模拟方法
- [[02_AI/AI-Infra/index|AI Infra]] — 通用推理基础设施

## Papers

- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 本笔记主要知识来源
- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 大尺度 VLA 边缘瓶颈分析
