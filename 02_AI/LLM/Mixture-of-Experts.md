---
title: Mixture-of-Experts
description: 通过稀疏激活的专家子网络扩展模型容量的神经网络架构
tags:
  - ai
  - architecture
  - moe
  - scaling
created: 2026-07-28
---

# Mixture-of-Experts

Mixture-of-Experts（MoE）是一种通过**稀疏激活多个专家子网络**来扩展模型容量的神经网络架构。

## Core Idea

将传统稠密层替换为多个并行的“专家”网络和一个“门控”网络。对于每个输入，门控网络只激活少量专家，从而在保持推理成本可控的同时显著增加模型参数量。

## Key Components

- **Experts**：并行的前馈子网络
- **Router / Gating Network**：决定每个 token 激活哪些专家
- **Top-k Routing**：通常只激活 top-1 或 top-k 个专家

## Why It Works

- 在相同计算预算下获得更大模型容量
- 不同专家可以学习不同模式或技能
- 适合大规模多任务场景

## Variants

- **Sparse MoE**：显式选择专家
- **Mixture-of-Transformers（MoT）**：在 Transformer 块级别混合多个子模型

## In Robotics

MoE 架构可用于构建大规模多模态生成模型，例如作为子目标图像生成的 world model backbone。

## Related Concepts

- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — MoE 可用于扩展 VLM 容量
- [[04_Embodied-AI/VLA/World-Model-for-Robotics|World Model for Robotics]] — 大规模生成模型可作为机器人世界模型

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 子目标图像生成 world model 基于 BAGEL（Mixture-of-Transformers）初始化
