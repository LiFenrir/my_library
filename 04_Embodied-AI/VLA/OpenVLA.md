---
title: "OpenVLA"
description: "开源的 7B 参数视觉-语言-动作模型，基于 Llama 2 与 DINOv2/SigLIP 构建"
tags: [concept, embodied-ai, vla, open-source]
created: 2026-07-30
---

# OpenVLA

**核心定义**：OpenVLA 是一个开源的 7B 参数 Vision-Language-Action（VLA）模型，基于 Llama 2 语言模型与 DINOv2/SigLIP 视觉编码器构建，在多个机器人数据集上训练，支持跨机器人 embodiment 的指令跟随。

## 核心特点

- **开源**：模型权重、训练代码与数据 pipeline 公开；
- **跨 embodiment 训练**：在多个机器人数据集（如 BridgeData V2、RT-1、Franka 等）上联合训练；
- **动作离散化**：将连续动作空间离散化为动作 token，与语言 token 统一建模；
- **可微调**：支持 LoRA 等参数高效微调以适应新机器人或任务。

## 架构

1. **视觉编码器**：DINOv2 + SigLIP 提取视觉特征；
2. **投影层**：将视觉特征映射到 LLM token 空间；
3. **语言模型**：Llama 2 7B；
4. **动作头**：输出离散动作 token。

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — OpenVLA 是 VLA 范式的代表实现
- [[04_Embodied-AI/VLA/VLA-Architecture|VLA Architecture]] — OpenVLA 采用的架构方案
- [[02_AI/LLM/Fine-Tuning|Fine-Tuning]] — OpenVLA 支持下游任务微调

## 来源

- Kim et al., 2024, "OpenVLA: An Open-Source Vision-Language-Action Model"
