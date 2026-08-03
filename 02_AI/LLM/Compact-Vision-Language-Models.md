---
title: Compact Vision-Language Models
description: 参数量通常在 0.5B–3B 之间、面向边缘部署的多模态模型类别。
tags:
  - ai
  - vlm
  - multimodal
  - edge-deployment
  - concept
created: 2026-07-28
---

# Compact Vision-Language Models

Compact VLMs 是参数规模在 **0.5B–3B** 之间、可在边缘 GPU 或高效 CPU 上运行的 Vision-Language Model，用于在内存和功耗受限环境中提供多模态推理能力。

## Why

大参数 VLM（如 Qwen2-VL 7B、LLaVA-1.5 13B）需要服务器级 GPU。Compact VLM 让视觉-语言能力进入机器人、无人机、AR 眼镜等边缘设备。

## Representative Models

| 模型 | 规模 | 特点 |
|------|------|------|
| **SmolVLM** | ~256M–2B | 高度压缩，保留语义推理，适合机器人控制 |
| **TinyLLaVA** | 1B–3B | 通过蒸馏压缩 LLaVA 架构 |
| **Qwen2-VL** | 2B–7B | 强视觉推理，但较大版本偏向服务器 |
| **PaliGemma** | ~3B | 多语言与视觉-文本对齐 |
| **Moondream2** | ~2B | 轻量图像描述与视觉 QA，适合 CPU 级边缘 |

## From VLM to VLA

Compact VLM 本身只输出文本，不能直接生成机器人动作。要用于闭环控制，通常需要：

1. 在机器人动作数据上监督微调，把动作也建模为 token。
2. 添加动作反量化层，把 token 映射为连续控制量。
3. 集成到低层控制器或 ROS 2 pipeline。

LiteVLA-Edge 直接使用 distilled SmolVLM-256M 作为 backbone，通过 image-to-action 微调实现边缘 VLA。

## Trade-offs

- **优点**：小体积、低延迟、可本地部署。
- **局限**：推理深度、长上下文、复杂规划能力弱于大模型。
- **关键问题**：视觉 token 数量与 projector 复杂度仍是 pre-fill 瓶颈。

## Related Concepts

- [[Vision-Language-Action|VLA]] — 把 compact VLM 变为动作生成模型
- [[LiteVLA-Edge|LiteVLA-Edge]] — SmolVLM-256M 的 VLA 部署案例
- [[Edge-VLA|Edge VLA]] — 边缘 VLA 设计空间

## Papers

- [[05_Papers/articles/litevla-edge|LiteVLA-Edge]]
- [[05_Papers/articles/litevla-h|LiteVLA-H]]

## Engineering

- 选择 compact VLM 时需同时评估：视觉编码器速度、projector 计算量、语言头容量。
- 在 VLA 场景中，backbone 的“动作稳定性”往往比通用 VQA 分数更重要。
