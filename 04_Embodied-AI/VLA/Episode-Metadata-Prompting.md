---
title: "Episode Metadata Prompting"
description: "将 episode 级别属性（速度、质量、是否犯错）作为提示注入 VLA 以解歧数据分布"
aliases:
  - Episode Metadata Conditioning
tags: [concept, embodied-ai, vla, prompting, conditioning, data-quality]
created: 2026-07-28
---

# Episode Metadata Prompting

将训练片段的属性标签作为 VLA 提示条件，使模型能够区分不同质量和策略的数据，并在测试时被引导到期望行为。

## 核心问题

真实机器人数据集包含成功、失败、次优自主数据等多种质量层次。没有元数据时，模型会对这些模式取平均，导致性能次优。元数据标签让模型知道每个片段“应该如何执行”。

## 常见元数据

| 属性 | 含义 | 示例 |
|------|------|------|
| Overall speed | episode 长度（步数） | "8000 steps" |
| Overall quality | 执行质量评分 1-5 | "Quality: 5" |
| Mistake | 该片段是否包含错误 | "Mistake: false" |
| Control Mode | 关节空间或末端执行器空间 | "joint" / "eef" |

## 训练

使用真实标注的元数据训练模型。每个元数据组件可独立随机丢弃：

- metadata 整体 dropout 约 15%
- 各组件单独 dropout 约 5%

使测试时能够灵活组合任意元数据条件。

## 推理

测试时通常设置：
- Speed：该任务较快的 episode 长度分位数
- Quality：最高等级
- Mistake：false

也可通过 [[02_AI/Generative-Models/Classifier-Free-Guidance|Classifier-Free Guidance]] 进一步增强期望行为。

## 优缺点

- **优点**：有效利用次优和失败数据；测试时可 steer 模型行为；无需为每种行为单独收集数据
- **缺点/局限**：需要额外标注；metadata 设计依赖任务领域知识；错误标注会误导模型

## Related Concepts

- [[04_Embodied-AI/VLA/Diverse-Prompting-for-VLA|Diverse Prompting for VLA]] — 元数据提示是其核心组件
- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]] — 与 metadata 同属多模态上下文条件
- [[02_AI/Generative-Models/Classifier-Free-Guidance|Classifier-Free Guidance]] — 可用于增强元数据条件
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]] — 接受元数据条件的策略

## Papers

- [[05_Papers/notes/pi0-7|π0.7]] — 通过 episode metadata 从次优和自主数据中学习，实现开箱即用的专家级性能
