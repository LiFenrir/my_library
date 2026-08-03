---
title: Noisy History Augmentation
description: 通过训练动作解码器适应部分去噪的视频历史，加速世界模型推理的数据增强技术
tags:
  - embodied-ai
  - world-model
  - video-generation
  - robot-control
  - training-technique
created: 2026-07-30
---

# Noisy History Augmentation

**Noisy History Augmentation** 是一种针对自回归视频-动作世界模型的训练技巧：在训练时向视频历史注入噪声，使动作解码器学会从部分去噪的视觉表示中预测动作，从而在推理时减少视频去噪步数、加速控制。

## Core Idea

视频 token 生成是世界模型推理的主要瓶颈。关键洞察是：**动作预测不需要像素级完美的视频表示**，只需鲁棒的语义结构即可推断控制指令。因此可以让动作网络适应"带噪"的视频历史，在推理时只把视频去噪到中等噪声水平。

## How It Works

训练时对历史视频隐状态 $z_{\leq t}$ 按一定概率加噪：

$$
\tilde{z}_{\leq t} = \begin{cases}
(1 - s_{\text{aug}})\epsilon + s_{\text{aug}} z_{\leq t}, & p = 0.5, \quad s_{\text{aug}} \in [0.5, 1], \quad \epsilon \sim \mathcal{N}(0, I) \\
z_{\leq t}, & p = 0.5
\end{cases}
$$

其中 $s_{\text{aug}}$ 控制加噪程度，与 flow matching 的插值方式一致。

## Inference Speedup

由于动作解码器对噪声历史具有鲁棒性，推理时视频 token 只需从 $s=0$ 积分到 $s=0.5$（而非 $s=1.0$），去噪步数减半，而动作预测质量基本保持。

## 优缺点

- **优点**：
  - 显著降低视频生成延迟；
  - 不增加模型参数量；
  - 与 flow matching 训练目标天然兼容。
- **缺点/局限**：
  - 过度加噪可能损失动作所需的空间细节；
  - 噪声调度需要针对任务平衡速度与精度。

## Related Concepts

- [[02_AI/Flow-Matching|Flow Matching]] — Noisy History Augmentation 的噪声插值基础
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 在自回归视频-动作世界模型中应用此技巧
- [[04_Embodied-AI/World-Model/Asynchronous-Inference-for-Robot-Control|Asynchronous Inference for Robot Control]] — 常与部分去噪配合实现实时控制
- [[04_Embodied-AI/VLA/Action-Chunking|Action Chunking]] — 同样用于降低单位时间推理开销

## Papers

- [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]] — 第 3.3 节提出 Noisy History Augmentation
