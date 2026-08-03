---
title: llama.cpp
description: 面向量化大语言模型的高性能 C++ 推理运行时，支持 CPU/GPU 多后端。
tags:
  - ai-infra
  - inference-runtime
  - llama-cpp
  - edge-inference
  - concept
created: 2026-07-28
---

# llama.cpp

llama.cpp 是一个用 C/C++ 编写的高性能 LLM 推理运行时，专注于量化模型在消费级和嵌入式硬件上的高效执行。

## Why

Python/PyTorch 运行时体积大、依赖重，不适合边缘部署。llama.cpp 提供：

- 高度优化的 CPU/GPU kernel
- 原生支持 GGUF 量化格式
- 跨平台（x86/ARM、CUDA、Metal、Vulkan）
- 低开销的推理服务封装

## Core Idea

通过手写 kernel、内存布局优化和量化计算，把大模型推理压缩到可在笔记本、树莓派、Jetson 等边缘设备上实时运行。

## Key Features

- **GGUF 原生支持**：4-bit/5-bit/8-bit 量化直接加载。
- **GPU offloading**：可将若干 transformer layer  offload 到 GPU，其余在 CPU。
- **KV-cache 管理**：可配置上下文长度以控制内存占用。
- **Batch / speculative decoding**：支持并发与投机解码加速。

## In Edge VLA

LiteVLA-Edge 使用 llama.cpp CUDA backend 部署 256M SmolVLM：

- 42 层全部 offload 到 Jetson AGX Orin GPU。
- `n_ctx=512`，最大输出 ≤12 token。
- 平均推理延迟 150.5 ms，抖动 σ < 0.2 ms。

## Configuration Notes

| 参数 | 典型设置 | 作用 |
|------|----------|------|
| `n_gpu_layers` | 42 | 全 GPU offloading |
| `n_ctx` | 512 | 限制 KV-cache |
| `n_predict` | ≤12 | 限制输出长度 |
| `temperature` | 0.0 | 确定性解码 |

## Related Concepts

- [[GGUF-Quantization|GGUF Quantization]] — llama.cpp 的主要模型格式
- [[LiteVLA-Edge|LiteVLA-Edge]] — llama.cpp 在 VLA 中的部署案例
- [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘推理延迟分析

## Engineering

- 全 GPU offloading 是降低延迟的关键，但受显存/统一内存限制。
- 上下文长度和输出 token 数直接影响 KV-cache 大小与推理时间。
- 对控制任务，建议使用确定性解码（T=0.0）以减少动作抖动。
