---
title: "02_AI"
description: "通用人工智能知识库：LLM、Agent、Prompt Engineering、AI Infra。"
tags: [moc, ai, llm, agent]
created: 2026-07-22
---

# 02_AI

通用人工智能知识资产。这里聚焦**不绑定具体硬件 embodiment** 的 AI 方法与系统：大语言模型、智能体、提示工程、AI 基础设施。

具身智能（VLA、World Model、机器人 RL 等）请移步 [[04_Embodied-AI/index|04_Embodied-AI]]。

## 子领域

- LLM — 大语言模型、预训练、对齐、推理
  - [[02_AI/LLM/index|LLM Index]] — 完整索引
  - [[02_AI/LLM/Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — 专业化训练与知识保持
- Agent — 智能体架构、工具使用、多智能体系统
  - [[02_AI/Agent/index|Agent Index]] — 完整索引
- VLM — 视觉语言模型、分割、跨模态理解
  - [[02_AI/VLM/index|VLM Index]] — 完整索引
  - [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — VLM 通用定义
- Cognitive-Architecture — 认知架构、自主智能体
  - [[02_AI/Cognitive-Architecture/index|Cognitive Architecture Index]]
  - [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]] — LeCun 的全可微自主智能体架构
  - [[02_AI/Cognitive-Architecture/Mode-1-Mode-2-Reasoning|Mode-1 / Mode-2 Reasoning]] — 反应性行为与基于世界模型的推理规划
  - [[02_AI/Cognitive-Architecture/Intrinsic-Cost|Intrinsic Cost]] — 不可训练的基础成本模块与内在动机
- Prompt-Engineering — 提示设计、模式、评估
  - [[02_AI/Prompt-Engineering/prompt-engineering|Prompt Engineering]] — 提示工程基础
  - [[02_AI/Prompt-Engineering/Prompt-Expansion|Prompt Expansion]] — 提示扩展
- AI-Infra — 训练/推理工程、分布式、模型服务
  - [[02_AI/AI-Infra/index|AI Infra Index]] — 完整索引
  - [[02_AI/AI-Infra/VLA-Inference|VLA Inference]] — VLA 推理延迟与调度入口

## 通用概念

- [[02_AI/Generative-Models/Flow-Matching|Flow Matching]] — 连续时间生成模型目标
- [[02_AI/Generative-Models/Classifier-Free-Guidance|Classifier-Free Guidance]] — 生成模型中的条件引导
- [[02_AI/General/Foundation-Model|Foundation Model]] — 基础模型总览
- [[02_AI/General/Model-in-the-Loop-Data-Engine|Model-in-the-Loop Data Engine]] — 模型驱动的数据迭代
- [[02_AI/General/Obsidian-Bidirectional-Links|Obsidian Bidirectional Links]] — 本库链接约定

## Skill 与工具

- [[02_AI/skills/index|Skills Index]] — 完整索引
- [[02_AI/skills/MinerU-PDF-to-Markdown|MinerU-PDF-to-Markdown]] — Claude Code skill，PDF/文档转 Markdown
- [[02_AI/skills/archive-papers|archive-papers]] — Claude Code skill，自动归档论文到 05_Papers

## 概念链

```
Concept → Theory → Paper → Engineering → Experiment → Project
```

相关入口：
- `01_Fundamentals` — 数学与 ML 基础
- [[04_Embodied-AI/index|04_Embodied-AI]] — 具身智能
- [[05_Papers/index|05_Papers]] — 论文精读
