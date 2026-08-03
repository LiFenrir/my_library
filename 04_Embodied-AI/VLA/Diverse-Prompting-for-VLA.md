---
title: Diverse Prompting for VLA
description: 在 VLA 训练与推理中使用多模态、多维度提示来解耦数据歧义并精确控制行为
tags:
  - embodied-ai
  - vla
  - prompting
  - conditioning
created: 2026-07-28
---

# Diverse Prompting for VLA

Diverse Prompting for VLA 指在 VLA 的训练与测试中引入**多种模态和维度的上下文提示**，以消除数据歧义、提升策略可控性并支持组合泛化。

## Motivation

大规模机器人数据通常包含：
- 不同质量的演示（成功、失败、次优）
- 不同执行策略（快/慢、不同控制模式）
- 不同任务阶段

单一任务描述无法区分这些模式，导致模型学到平均行为。Diverse Prompting 通过丰富上下文让模型知道“做什么”以及“怎么做”。

## Prompt Components

- **任务指令** $\ell$：高层目标描述
- **子任务指令** $\hat{\ell}$：当前阶段的具体语义目标
- **子目标图像** $g$：期望的近期视觉状态
- **Episode Metadata** $m$：速度、质量、错误等标签
- **控制模式** $c$：关节空间或末端执行器空间控制

## Training with Dropout

每个提示组件在训练中随机丢弃，使模型在测试时能够灵活使用任意子集。

## Benefits

- 从次优和自主数据中学习而不损害性能
- 测试时可通过调整提示选择不同行为模式
- 支持语言辅导和自动高层策略

## Related Concepts

- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]] — 使用图像作为提示
- [[04_Embodied-AI/VLA/Episode-Metadata-Conditioning|Episode Metadata Conditioning]] — 使用元数据作为提示
- [[02_AI/Prompt-Engineering/Prompt-Expansion|Prompt Expansion]] — 提示扩展的通用概念
- [[02_AI/Classifier-Free-Guidance|Classifier-Free Guidance]] — 可应用于提示组件的引导技术

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 提出并验证了多模态 diverse prompting 在 VLA 中的有效性
