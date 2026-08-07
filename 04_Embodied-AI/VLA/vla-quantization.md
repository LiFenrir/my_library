---
title: "VLA Quantization"
description: "将 VLA 权重压缩到低位宽以实现边缘设备部署的技术"
tags: [concept, embodied-ai, vla, edge-ai, quantization]
created: 2026-07-29
---

# VLA Quantization

**核心定义**：VLA Quantization 是将 Vision-Language-Action 模型的权重（有时包括激活）从 FP32/FP16 压缩到 INT8/INT4 等低位宽表示，以降低边缘设备上的内存占用、带宽需求和推理延迟。

## 常见方法

| 方法 | 说明 |
|------|------|
| INT8/FP16 | 标准精度降低 |
| 4-bit GGUF (Q4_K_M) | llama.cpp 常用格式，平衡压缩率和精度 |
| AWQ/GPTQ | 感知激活的权重量化 |
| 知识蒸馏 + 量化 | 先蒸馏小模型再量化 |

## 边缘部署中的挑战

- **Action Drift**：量化误差可能导致连续动作命令的精度下降，产生不稳定行为
- **视觉编码器敏感**：VLM 的视觉部分对量化更敏感
- **KV-cache 开销**：长上下文下 KV-cache 可能成为新的内存瓶颈

## LiteVLA-Edge 实例

- 256M 参数 SmolVLM backbone
- FP32 监督微调 + LoRA (r=8, α=8)
- 转换为 GGUF 4-bit (Q4_K_M)
- 在 Jetson AGX Orin 上通过 llama.cpp CUDA 后端推理
- 平均延迟 150.5 ms (~6.6 Hz)

## 优缺点

- **优点**：显著降低模型大小和内存带宽、可在资源受限设备运行、保持基本语义能力
- **缺点/局限**：需要验证动作稳定性、可能损失精度、调试复杂

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Actio[[02_AI/AI-Infra/VLA-Inference|VLA Inference]]|Vision-Language-Action Mode[[02_AI/AI-Infra/VLA-Inference|VLA Inference]] — 量化的对象
- [[02_AI/AI-Infra/VLA-Inference|VLA Inference]]|VLA Inference Latenc[[02_AI/AI-Infra/VLA-Inference|VLA Inference]] — 量化试图解决的核心问题
- [[04_Embodied-AI/VLA/Dual-Rate-VLA-Scheduling|Dual-Rate VLA Schedulin[[02_AI/AI-Infra/VLA-Inference|VLA Inference]] — 另一种边缘优化策略

## 来源

- [[05_Papers/articles/litevla-edge|LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotic[[02_AI/AI-Infra/VLA-Inference|VLA Inference]]，第 IV 节
