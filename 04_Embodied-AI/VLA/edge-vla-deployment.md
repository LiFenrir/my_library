---
title: "Edge VLA Deployment"
description: "在资源受限边缘设备上部署和运行 VLA 的系统工程问题"
tags: [concept, embodied-ai, vla, edge-ai, robotics]
created: 2026-07-29
---

# Edge VLA Deployment

**核心定义**：Edge VLA Deployment 关注如何在功耗、内存、计算受限的边缘设备（如 NVIDIA Jetson、Raspberry Pi）上部署和运行 Vision-Language-Action 模型，以满足机器人实时控制的延迟要求。

## 关键约束

- **功耗**：通常 25W–40W
- **延迟**：安全操作需要 10–20 Hz 控制频率
- **内存**：统一内存有限
- **确定性**：需要低抖动、可预测推理时间
- **离线运行**：GPS-denied 或网络不稳定环境

## 常用技术

| 技术 | 作用 |
|------|------|
| 模型压缩 | 量化、剪枝、蒸馏 |
| 紧凑 backbone | SmolVLM、PaliGemma、TinyLLaVA |
| 优化运行时 | llama.cpp、TensorRT、ONNX Runtime |
| 异步流水线 | 推理与低层控制解耦 |
| 分层架构 | 高层语义 + 高频动作 token |

## 系统架构要点

- 感知-推理-执行模块化
- VLA 输出结构化命令（如 Twist）
- 低层控制器保持高频率心跳（如 100 Hz）
- 安全覆盖和确定性解析器必不可少

## 与 Cloud-Edge 混合方案的区别

- Cloud-Edge 混合：重推理在云端，本地只运行简单控制环
- Fully On-Device：所有推理在本地完成，不依赖网络

## 与其他概念的关系

- [[04_Embodied-AI/VLA/vla-quantization|VLA Quantization]] — 边缘部署的核心压缩技术
- [[02_AI/AI-Infra/vla-inference-latency|VLA Inference Latency]] — 边缘部署需要优化的核心指标
- [[04_Embodied-AI/VLA/Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 边缘调度策略

## 来源

- [[05_Papers/articles/litevla-edge|LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics]]，第 I、III、IV 节
