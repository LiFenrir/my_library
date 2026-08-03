---
title: Edge VLA
description: 面向嵌入式平台、强调低延迟本地推理的 Vision-Language-Action 系统类别。
tags:
  - embodied-ai
  - vla
  - edge-deployment
  - real-time
  - concept
created: 2026-07-28
---

# Edge VLA

Edge VLA 指专为**资源受限嵌入式平台**设计的 Vision-Language-Action 系统，目标是在本地实现低延迟、低功耗、可闭环的视觉-语言-动作推理。

## Why

通用 VLA（如 OpenVLA 7B）依赖桌面/云端 GPU，无法满足以下场景：

- 功率受限的 field robots（25W–40W 功耗包络）
- GPS 拒止、带宽受限环境
- 战术或安全关键应用，要求本地、离线执行
- 需要 <200 ms 反应时间的闭环控制

## Core Idea

在 compact backbone、量化压缩、专用推理运行时和软硬件协同设计之间取得平衡，把 VLA 从“开环推理”推进到“实时 visuomotor 控制”。

## Design Space

| 维度 | 选择 |
|------|------|
| Backbone | 256M–1B compact VLM（如 SmolVLM、TinyLLaVA） |
| 量化 | INT4/INT8、GGUF、TensorRT、ONNX |
| 运行时 | llama.cpp、TensorRT-LLM、vLLM edge |
| 调度 | 单速率、双速率（动作+语义）、事件触发 |
| 集成 | ROS 2、裸机、微控制器接口 |
| 输出 | 单 action token、action chunk、外环引导 |

## Representative Systems

- [[OpenVLA]]：7B 通用 VLA，桌面 GPU，zero-shot 泛化强。
- **EdgeVLA**：~1B，分层语义/动作 token，10–15 Hz。
- **EfficientVLA**：蒸馏 + action chunking，TensorRT。
- **LiteVLA-Edge**：256M，GGUF + llama.cpp，Jetson Orin，6.6 Hz。
- **LiteVLA-H**：在 LiteVLA-Edge 基础上引入双速率调度，动作 19.74 Hz。
- **AnywhereVLA**：450M，移动操作与探索。

## Related Concepts

- [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘 VLA 的 pre-fill 主导延迟特征
- [[Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 双速率动作/语义调度
- [[Vision-Language-Action|VLA]] — VLA 范式总览
- [[LiteVLA-Edge|LiteVLA-Edge]] — 具体部署系统
- [[02_AI/AI-Infra/index|AI Infra]] — 通用推理基础设施

## Papers

- [[05_Papers/articles/litevla-edge|LiteVLA-Edge]]
- [[05_Papers/articles/litevla-h|LiteVLA-H]]

## Engineering

- 边缘 VLA 的核心瓶颈通常是**多模态 pre-fill**，而非解码 token 数量。
- 优先优化：视觉 token 数量、projector 复杂度、提示缓存、GPU offloading。
- 安全：VLA 输出应作为外环引导，底层控制器负责高频率稳定与急停。

## Questions

- 6–10 Hz 是否是通用机器人闭环控制的最低可用频率？
- 不同 embodiment（无人机、机械臂、移动底盘）对 Edge VLA 的延迟要求差异多大？
- 量化导致的动作漂移如何通过训练或后处理补偿？
