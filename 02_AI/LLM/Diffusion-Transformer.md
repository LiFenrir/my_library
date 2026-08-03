---
title: Diffusion Transformer
description: 将扩散模型与 Transformer 架构结合，用于高质量序列/图像/动作生成的生成模型
tags:
  - generative-model
  - diffusion
  - transformer
  - concept
created: 2026-07-30
---

# Diffusion Transformer (DiT)

Diffusion Transformer（DiT）将**扩散模型（Diffusion Model）**的噪声到数据生成过程与**Transformer**的序列建模能力结合，用一个 Transformer 骨干替代传统的 U-Net 骨干，实现高质量的生成。

## Core Idea

扩散模型通过多步去噪从纯噪声生成数据：

```
x_T ~ N(0, I) → 逐步去噪 → x_0 (数据)
```

传统扩散模型使用 U-Net 作为去噪网络；DiT 则把输入 patch 化为 token，用 Transformer 预测噪声或速度场，从而：

- 利用 Transformer 的长程依赖建模能力。
- 更方便地扩展模型规模（符合缩放律）。
- 与 LLM/VLM 的 token 化接口更一致。

## Architecture

典型 DiT 包含：

1. **Patch Embedding**：将图像/动作/特征序列切分为 token。
2. **Transformer Blocks**：标准自注意力 + 前馈网络，通常注入条件（时间步、文本/视觉条件）。
3. **Output Head**：预测噪声、速度 `v` 或直接预测去噪后的数据。

条件注入方式包括 AdaLN（Adaptive LayerNorm）、交叉注意力等。

## In VLA / Robotics

在 Vision-Language-Action 模型中，DiT 可用于**连续动作生成**：

- 输入：视觉-语言条件 + 噪声动作序列。
- 输出：平滑、高频的关节或末端执行器轨迹。

相比离散动作 tokenization，DiT 更擅长生成连续、平滑、多步的动作轨迹。

## Trade-offs

- **推理步数**：扩散模型通常需要多步去噪，首 token/动作延迟较高。
- **实时性**：在边缘 10–20 Hz 控制约束下，多步生成可能成为瓶颈。
- **质量 vs 速度**：可通过蒸馏、少步采样、确定性采样器折中。

## Related Concepts

- [[Flow-Matching|Flow Matching]] — 另一种连续生成路径学习方法
- [[Classifier-Free-Guidance|Classifier-Free Guidance]] — 扩散/流模型中常用的条件控制技术
- [[Action-Tokenization|Action Tokenization]] — 与 DiT 相对的离散动作表示方法
- [[VLA-Architecture|VLA Architecture]] — DiT 在 VLA 动作生成模块中的位置

## Papers

- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 将 DiT 列为 VLA 连续动作生成的典型解码器
