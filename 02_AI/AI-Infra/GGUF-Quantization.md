---
title: GGUF Quantization
description: GGML 通用文件格式与后训练量化技术，常用于边缘 LLM/VLM/VLA 部署。
tags:
  - ai-infra
  - quantization
  - gguf
  - edge-inference
  - concept
created: 2026-07-28
---

# GGUF Quantization

GGUF（GGML Universal File Format）是 llama.cpp 生态的模型文件格式，支持多种后训练量化方案，用于在资源受限设备上部署大模型。

## Why

边缘设备（如 Jetson Orin）内存与带宽有限。GGUF 通过 4-bit/8-bit 量化显著减小模型体积，同时提供高度优化的 CPU/GPU kernel，降低推理延迟。

## Core Idea

将 FP32/FP16 权重转换为低精度整数表示，配合量化尺度（scale）与零点（zero-point）在推理时反量化。GGUF 将权重、配置、tokenizer 等打包为单一文件，便于跨平台分发。

## Common Quantization Schemes

| 方案 | 说明 | 典型用途 |
|------|------|----------|
| Q4_K_M | 4-bit，K-quants，中等混合 | 边缘 GPU，平衡精度与体积 |
| Q5_K_M | 5-bit，更高精度 | 对数值敏感的任务 |
| Q8_0 | 8-bit，精度损失小 | 内存允许时优先 |
| FP16 | 半精度 | 训练后微调的中间格式 |

## In VLA Deployment

LiteVLA-Edge 使用 Q4_K_M 对 256M SmolVLM backbone 进行后训练量化：

- 训练阶段使用 FP32 保持动作精度。
- 部署阶段转换为 GGUF，整个模型驻留在 Orin 统一内存。
- 通过 llama.cpp CUDA backend 全 GPU offloading 推理。

## Trade-offs

- **优点**：体积小、加载快、跨平台、llama.cpp 高度优化。
- **风险**：动作漂移（action drift）——低精度可能降低连续控制量的数值稳定性。
- **缓解**：FP32 训练、后训练量化、确定性解码、结构化动作解析与安全覆盖。

## Related Concepts

- [[llama-cpp|llama.cpp]] — 主要 GGUF 推理运行时
- [[LiteVLA-Edge|LiteVLA-Edge]] — 使用 GGUF 的 VLA 部署案例
- [[Edge-VLA|Edge VLA]] — 边缘 VLA 设计空间

## Papers

- [[05_Papers/articles/litevla-edge|LiteVLA-Edge]]

## Engineering

- 量化应在训练完成后进行，避免训练期间精度损失影响策略学习。
- 对机器人控制任务，建议验证量化前后动作分布的一致性。
- 选择量化方案时需在模型大小、推理速度和动作稳定性之间权衡。
