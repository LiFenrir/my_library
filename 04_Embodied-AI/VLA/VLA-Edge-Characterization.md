---
title: VLA Edge Characterization
description: 基于 MolmoAct-7B 在 Jetson Orin/Thor 上的实测，识别 VLA 动作生成阶段的内存带宽瓶颈并投影至 100B 模型
tags:
  - embodied-ai
  - vla
  - edge-inference
  - latency
  - scaling
created: 2026-07-28
---

# VLA Edge Characterization

大参数 VLA 在边缘部署时，**动作生成阶段（action generation / autoregressive decoding）是主要延迟瓶颈**。该结论来自对 MolmoAct-7B 在 NVIDIA Jetson AGX Orin 与 Jetson Thor 上的实测与模拟投影。

## Why

- 机器人任务性能遵循神经缩放律（neural scaling laws），要达到复杂真实环境的通用能力，模型规模需达到 10–100B。
- 安全动态操作要求控制频率至少 10–20 Hz。
- 当代边缘加速器擅长稠密计算，但对稀疏、内存受限的自回归解码支持不足。

## 关键发现

### 1. 生成阶段是主要瓶颈

在 MolmoAct-7B 的端到端单步延迟中：

- **Generation（自回归解码 + 推理）**：约占 **75%**。
- Vision Encoder：约占 20%。
- Action Transformer：约占 5%。

当前边缘平台延迟约为实时目标（10 Hz）的 **200–300 倍**。

### 2. 生成阶段内存带宽受限

Jetson Thor 的 BF16 算力约为 Orin 的 5 倍，但端到端延迟仅提升约 **1.4 倍**。说明瓶颈在**内存带宽**而非算力。

### 3. 硬件 scaling 仍不足

通过 XPU 模拟器将模型从 7B 扩展到 100B，并在假设的 GDDR7、PIM 等增强内存系统上评估：

- 更高带宽的 GDDR7、PIM 能显著改善控制频率。
- 但即使采用 PIM，100B 模型仍难以稳定达到 10–20 Hz 目标。

## 两个边缘 VLA  regime 的对比

| 特征 | Compact Edge VLA | Large Spatial-Reasoning VLA |
|------|------------------|----------------------------|
| 典型规模 | 256M–7B | 10B–100B |
| 主导延迟 | Pre-fill（视觉编码 + projector） | Action Generation（自回归解码） |
| 优化重点 | 减少视觉 token、缓存提示结构 | 提升内存带宽、算法-系统协同设计 |
| 代表观察 | TTFA 占 ~94% | 生成阶段占 ~75% |

参见 [[Edge-VLA-Inference|Edge VLA Inference]] 对 compact regime 的分析。

## 工程含义

- 单纯提升 SoC 算力无法解决大 VLA 的实时性问题。
- 需要算法-系统协同优化：更高效的解码、内存层级优化、近存计算/存内计算等。
- 在边缘完全自治的通用机器人仍需突破内存墙。

## Related Concepts

- [[VLA-Architecture|VLA Architecture]] — VLA 的三阶段计算架构
- [[Edge-VLA-Inference|Edge VLA Inference]] — 紧凑边缘 VLA 的 pre-fill 主导延迟分析
- [[Outer-Loop-Guidance|Outer-Loop Guidance]] — 用外环引导降低 VLA 实时控制压力
- [[Roofline-Model|Roofline Model]] — 解释内存带宽受限现象的性能模型
- [[AI-Edge-Performance-Evaluation|AI Edge Performance Evaluation]] — 本文使用的硬件评测与模拟方法

## Papers

- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 本笔记主要知识来源
