---
title: Episode Metadata Conditioning
description: 将训练片段的质量、速度、错误等元数据作为提示条件，使 VLA 能从多样化数据中学习并精确控制行为模式
tags:
  - embodied-ai
  - vla
  - conditioning
  - data-quality
created: 2026-07-28
---

# Episode Metadata Conditioning

Episode Metadata Conditioning 是将**训练片段的属性标签**作为 VLA 提示条件的技术，使模型能够区分不同质量和策略的数据。

## Motivation

真实机器人数据集包含成功、失败、次优自主数据等多种质量层次。没有元数据时，模型会平均这些模式，导致性能下降。元数据标签让模型知道每个片段“应该如何执行”。

## Common Metadata Labels

- **Overall Speed**：片段长度（离散化为步数区间）
- **Overall Quality**：任务执行质量评分（如 1–5 分）
- **Mistake**：当前动作段是否包含错误
- **Control Mode**：关节空间或末端执行器空间

## Training

使用真实标注的元数据训练模型。每个元数据组件可独立随机丢弃，使测试时能够灵活组合。

## Inference

测试时通常设置：
- Speed：该任务较快的 episode 长度分位数
- Quality：最高等级
- Mistake：false

也可通过 [[02_AI/Classifier-Free-Guidance|Classifier-Free Guidance]] 进一步增强期望行为。

## Benefits

- 从混合质量数据中持续学习
- 蒸馏专家策略的行为（通过标注专家 rollout 的高质量元数据）
- 测试时精确控制速度、质量等行为属性

## Related Concepts

- [[04_Embodied-AI/VLA/Diverse-Prompting-for-VLA|Diverse Prompting for VLA]] — 元数据提示是其核心组件
- [[02_AI/Classifier-Free-Guidance|Classifier-Free Guidance]] — 可用于增强元数据条件
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 接受元数据条件的策略

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 通过 episode metadata 从次优和自主数据中学习，实现开箱即用的专家级性能
