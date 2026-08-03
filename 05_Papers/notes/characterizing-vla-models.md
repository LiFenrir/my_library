---
title: "Characterizing VLA Models: Identifying the Action Generation Bottleneck for Edge AI Architectures"
description: "在 Jetson Orin/Thor 上剖析 VLA 推理瓶颈，指出动作生成阶段占 75% 延迟。"
tags: ["VLA", "Edge-AI", "Hardware-Characterization", "Bottleneck-Analysis", "PIM", "Memory-Bandwidth", "Jetson"]
created: 2026-07-15
---

# Characterizing VLA Models: Identifying the Action Generation Bottleneck for Edge AI Architectures

## 基本信息
- **作者**: Manoj Vishwanathan (Google / Purdue University), Suvinay Subramanian (Google), Anand Raghunathan (Purdue University)
- **机构**: Google, Purdue University
- **链接**: [arXiv:2603.02271](https://arxiv.org/abs/2603.02271)
- **发表**: arXiv preprint, 2026

## 研究背景与动机

VLA 模型遵循神经扩展律（neural scaling laws），要实现通用机器人能力需要扩展到 10-100B 参数。然而实时部署需要 **10-20 Hz** 的控制频率，当前边缘加速器在结构上不适合 VLA action generation 的稀疏、memory-bound 自回归处理。

现有系统如 Gemini Robotics 1.5 采用"双脑"架构：强大模型在云端推理，本地只维持基本控制回路——这在低延迟全自主边缘系统中不实用。本文通过**系统性的 VLA 工作负载特征分析**来指导下一代边缘系统设计。

## 核心方法

### VLA 计算架构

将 VLA 分解为三个子系统：

1. **Vision Encoder (感知核心)**：SigLIP + DINOv2 融合主干，提取视觉特征嵌入，通过 MLP projector 映射到推理引擎的嵌入空间
2. **Generation (推理引擎)**：decoder-only Transformer，处理视觉+文本 token 的级联序列，可能产生 CoT 推理或空间 waypoint
3. **Action Transformer**：将内部表示转化为电机指令（离散动作 tokenization 或连续 DiT 解码）

### 混合评估方法

- **真实硬件 Profiling**：在 Jetson AGX Orin (64GB) 和 Jetson Thor (128GB) 上使用 NVIDIA Nsight Compute 对 MolmoAct-7B 进行 kernel 级性能追踪
- **模拟器投影**：使用自研 XPU 模拟器（70-90% 精度），对 7B-100B 参数模型在现有和假设硬件配置上进行投影

## 核心发现

### 1. 延迟瓶颈：75% 来自 Action Generation

- MolmoAct-7B 端到端延迟约为实时需求的 **200-300×**
- **Generation 阶段（自回归解码+推理）占约 75% 的端到端延迟**
- 该阶段主要是 **memory bandwidth bound**——Thor 相比 Orin 提供 5× 算力，但端到端延迟仅提升 1.4×

![[99_Attachments/papers/images/characterizing-vla-models/vla_bottleneck_fig2_performance.jpg]]

### 2. 硬件规格对比

| 硬件              | 内存类型        | 带宽 (GB/s) | BF16 TFLOPS |
| --------------- | ----------- | --------- | ----------- |
| Orin            | LPDDR5      | 203       | 100         |
| Thor            | LPDDR5X     | 273       | 500         |
| Orin+GDDR7 (假设) | GDDR7       | 1000      | 100         |
| Thor+PIM (假设)   | LPDDR6X PIM | 2180      | 3993        |

### 3. 架构投影：更大模型仍不达标

- 即使配备 GDDR7 和 PIM，100B 参数模型在边缘设备上仍远低于 10-20 Hz 目标
- 单纯的内存扩展不足以在交互速率下处理 10-100B 参数模型
- 需要**算法-系统协同设计**的全新方案

## 个人思考与启发

1. **瓶颈明确定位**：本文通过精确 profiling 确认了 VLA 的主要瓶颈是 memory-bound 的 generation 阶段而非 vision encoding，这对硬件加速器设计有直接指导意义。

2. **与 LiteVLA-Edge 系列的对比**：LiteVLA-Edge/H 从模型侧解决问题（压缩到 256M + 量化 + 调度优化），本文从硬件侧分析瓶颈并探索未来架构。两者互补：一个给出当下可行的方案，一个指出未来的硬件需求。

3. **PIM（Processing-in-Memory）的前景**：在内存带宽瓶颈场景下，PIM 是自然的技术路径，但即使最激进的 PIM 配置也难以支撑 100B 模型。这暗示模型压缩和硬件创新需要同步推进。

4. **"5× 算力 ≠ 5× 加速"的教训**：Thor 5× 算力仅带来 1.4× 延迟改善，强烈说明 memory wall 是真实瓶颈。对系统设计者来说，高带宽内存（HBM、GDDR7）比更多 FLOPS 更重要。

5. **可改进方向**：
   - 本文的模拟器精度（70-90%）有提升空间
   - 缺乏对更多 VLA 架构（如 Flow-based VLA）的分析
   - PIM 假设过于理想化，需考虑实际 PIM 的编程复杂性和热约束

## 相关论文

- RT-2: Vision Language Action Models Transfer Web Knowledge to Robotic Control (arXiv:2307.15818)
- MolmoAct: Action Reasoning Models that can Reason in Space (arXiv:2508.07917)
- Neural Scaling Laws in Robotics (arXiv:2405.14005)
- Gemini Robotics 1.5 (arXiv:2510.03342)


## 原文

[[05_Papers/articles/characterizing-vla-models|characterizing-vla-models]]
