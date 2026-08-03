---
title: VLA Architecture
description: Vision-Language-Action 模型的三阶段计算架构：视觉编码器、生成式推理引擎、动作变换器
tags:
  - embodied-ai
  - vla
  - concept
  - multimodal
  - robotics
created: 2026-07-28
---

# VLA Architecture

Vision-Language-Action（VLA）模型是一类将**视觉感知、自然语言理解与物理动作**统一的多模态基础模型。其计算架构通常可分解为三个主要子系统。

## 1. Vision Encoder（感知核心）

将原始像素转换为结构化特征嵌入。

- 常用骨干：SigLIP、DINOv2 等融合骨干，同时捕获语义上下文与空间几何细节。
- 投影器（Projector）：通常是多层 MLP，将高维视觉特征映射到推理引擎的嵌入空间。
- 计算特征：高并行、计算密集，但通常不是长序列生成的瓶颈。

## 2. Generation（推理引擎）

核心是一个 decoder-only Transformer，处理视觉与文本 token 拼接后的序列。

- 执行跨模态推理，可能生成中间输出，例如 Chain-of-Thought（CoT）推理或空间路径点。
- 将高层语言指令分解为可执行计划。
- 计算特征：自回归解码，内存带宽受限，通常是端到端延迟的主要贡献者。

## 3. Action Transformer（动作变换器）

将模型内部表示转换为机器人运动指令。

- **离散动作 tokenization**：将连续动作空间量化成 bin，作为离散 token 在词表中预测。
- **连续动作生成**：使用 Diffusion Transformer（DiT）等专用解码器，输出平滑的关节或末端执行器轨迹。

## 性能瓶颈

根据硬件特征分析，VLA 推理的主要瓶颈是：

- **Action Generation / Autoregressive Decoding**：约占 75% 端到端延迟
- 该阶段通常是 memory-bound 而非 compute-bound
- 因此增加计算能力（如 Thor 相比 Orin）提升有限，需要更高内存带宽

## 与相关概念的关系

- [[Vision-Language-Model|Vision Language Model]] — VLA 的视觉-语言基础
- [[Edge-VLA-Inference|Edge VLA Inference]] — 紧凑边缘 VLA 的延迟特征
- [[VLA-Edge-Characterization|VLA Edge Characterization]] — 大尺度 VLA 在边缘硬件上的瓶颈分析
- [[Outer-Loop-Guidance|Outer-Loop Guidance]] — 动作 token 作为外环引导的控制层级
- [[Chain-of-Thought-Reasoning|Chain-of-Thought Reasoning]] — 生成/推理引擎的中间推理步骤
- [[Diffusion-Transformer|Diffusion Transformer]] — 连续动作生成的典型解码器

## Papers

- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 三阶段架构与边缘硬件瓶颈的系统性分析
- [[RT-2]] — VLA 范式的代表性工作
