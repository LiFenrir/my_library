---
title: LiteVLA-Edge
description: 面向 NVIDIA Jetson AGX Orin 的量化本地 VLA 部署系统，实现约 150 ms 端到端推理。
tags:
  - embodied-ai
  - vla
  - edge-deployment
  - jetson-orin
  - ros2
  - concept
created: 2026-07-28
---

# LiteVLA-Edge

LiteVLA-Edge 是一个**部署导向的 VLA pipeline**，在 NVIDIA Jetson AGX Orin 上实现完全本地、离线的视觉-语言-动作推理，平均端到端延迟约 150.5 ms（~6.6 Hz）。

## Why

大参数 VLA（如 OpenVLA 7B）需要桌面级 GPU 或云端计算，难以部署在功率受限（25W–40W）的嵌入式机器人上。LiteVLA-Edge 探索 compact VLA 在真实边缘硬件上的实时闭环控制可行性。

## Core Idea

将监督式 image-to-action 微调与**后训练 4-bit GGUF 量化**结合，在保持动作稳定性的同时把 256M 参数模型塞进 Jetson Orin 的统一内存。

## System Architecture

感知-推理-动作三段式 pipeline：

1. **Vision encoder** 处理 RGB 帧，生成视觉 token。
2. **Multimodal transformer**（distilled SmolVLM-256M）融合视觉与语言目标。
3. **Action decoder** 输出结构化动作 token。
4. **ROS 2 bridge** 解析为 `geometry_msgs/Twist`，发布给底层控制器。

模块化设计允许确定性安全覆盖与更简单的调试。

## Training & Compression

- **微调**：FP32 全精度监督 image-to-action 微调，LoRA rank r=8，α=8。
- **量化**：训练后转换为 GGUF 格式，使用 4-bit Q4_K_M 量化。
- **运行时**：llama.cpp CUDA backend，42 层全部卸载到 Orin GPU。
- **上下文**：`n_ctx=512`，最大输出 ≤12 token，以减小 KV-cache 开销。

## Key Results

| 指标 | 数值 |
|------|------|
| 平均延迟 | 150.5 ms |
| 推理频率 | ~6.6 Hz |
| 延迟标准差 | 0.13 ms |
| 模型参数 | 256M |
| 平台 | Jetson AGX Orin |

## Positioning

- **OpenVLA**：7B 通用模型，桌面 GPU，强调 zero-shot 泛化。
- **EdgeVLA**：~1B，AGX Orin/A100，10–15 Hz，分层语义与动作 token。
- **EfficientVLA**：蒸馏 + action chunking，依赖 TensorRT。
- **LiteVLA-Edge**：256M，纯本地 GGUF/llama.cpp，强调可移植与模块化 ROS 2 集成。

## Related Concepts

- [[Vision-Language-Action|VLA]] — VLA 范式总览
- [[Edge-VLA|Edge VLA]] — 边缘 VLA 设计空间
- [[Edge-VLA-Inference|Edge VLA Inference]] — pre-fill 主导的延迟分析
- [[Action-Tokenization|Action Tokenization]] — 动作 token 与反量化
- [[VLA-ROS2-Integration|VLA-ROS2 Integration]] — 与 ROS 2 的集成工程
- [[GGUF-Quantization|GGUF Quantization]] — 4-bit 量化技术
- [[llama-cpp|llama.cpp]] — 边缘推理运行时

## Papers

- [[05_Papers/articles/litevla-edge|LiteVLA-Edge]] — 本笔记主要来源
- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 在 LiteVLA-Edge 基础上引入双速率调度

## Engineering

- 全 GPU offloading、上下文截断、GGUF kernel 优化是达到 6.6 Hz 的关键。
- ROS 2 节点异步订阅相机、发布速度指令，低层控制器维持 100 Hz 心跳。

## Questions

- 150 ms 阈值是否足以支持更灵巧的抓取/操作任务？
- 4-bit 量化对连续控制精度的长期影响如何量化？
- 在更弱的 Orin NX/Nano 上是否需要进一步剪枝或降低精度？
