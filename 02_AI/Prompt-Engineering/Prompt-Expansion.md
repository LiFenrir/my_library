---
title: Prompt Expansion
description: 通过自动补充更详细的上下文信息来增强基础模型可控性的提示技术
tags:
  - ai
  - prompt-engineering
  - multimodal
  - conditioning
created: 2026-07-28
---

# Prompt Expansion

Prompt Expansion 是一种通过**为原始提示自动补充更丰富的上下文信息**，来增强生成模型可控性与质量的提示技术。

## Core Idea

原始用户提示往往过于简略或存在歧义。通过扩展提示（例如添加详细描述、风格标签、子目标、元数据等），模型能够更准确地理解意图并生成符合要求的结果。

## Common Forms

- **文本扩展**：将简短指令改写为详细描述
- **多模态扩展**：补充图像、视频、音频等条件
- **元数据扩展**：添加质量、速度、风格等结构化标签

## Why It Works

- 减少训练数据中的模式平均问题
- 使模型能够区分不同质量和风格的样本
- 在测试时可通过调整提示精确控制生成行为

## In Robotics

Prompt Expansion 是 π0.7 的核心思想：通过为训练片段添加子任务指令、子目标图像、episode metadata 等多模态提示，使 VLA 能够从多样化数据中学习并精确控制行为。

## Related Concepts

- [[04_Embodied-AI/VLA/Diverse-Prompting-for-VLA|Diverse Prompting for VLA]] — 在 VLA 中的具体实现
- [[04_Embodied-AI/VLA/Episode-Metadata-Conditioning|Episode Metadata Conditioning]] — 通过元数据扩展提示
- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]] — 通过图像扩展提示
- [[02_AI/Classifier-Free-Guidance|Classifier-Free Guidance]] — 常与扩展提示结合使用

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 提出并验证了 VLA 中的多模态 prompt expansion
