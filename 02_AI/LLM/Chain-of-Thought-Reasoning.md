---
title: Chain-of-Thought Reasoning
description: 让模型生成中间推理步骤再得出答案或动作的推理方式
tags:
  - llm
  - reasoning
  - chain-of-thought
  - concept
created: 2026-07-30
---

# Chain-of-Thought Reasoning (CoT)

Chain-of-Thought（CoT，思维链）是一种让模型在给出最终输出之前，先生成一系列中间推理步骤的提示/训练技术。通过显式展开推理过程，模型在复杂任务上的准确性和可解释性通常优于直接预测答案。

## Core Idea

传统方式：

```
输入问题 → 直接输出答案
```

CoT 方式：

```
输入问题 → 中间推理步骤 → 最终答案
```

这些中间步骤通常以自然语言形式呈现，把多跳推理拆解为可验证的子步骤。

## Why

- **复杂问题分解**：将高层目标拆分为可执行的子目标或判断条件。
- **可解释性**：推理路径可被人类检查，定位错误来源。
- **提升准确性**：在数学、符号推理、多步决策等任务中效果显著。

## In VLA / Robotics

在 Vision-Language-Action 模型中，CoT 不仅限于文本推理，还可以表现为：

- **文本形式的推理链**：模型先解释“为什么要这样做”，再输出动作 token。
- **空间路径点（spatial waypoints）**：把高层语言指令分解为中间空间目标，再生成最终动作。
- **动作计划**：先生成粗略计划，再细化到具体关节或末端执行器轨迹。

通过这种方式，VLA 能把抽象的语义指令转化为结构化的可执行计划。

## Trade-offs

- **延迟增加**：每多生成一个推理 token，都会增加自回归解码步数。
- **可靠性**：中间步骤可能出错，并传播到最终动作。
- **边缘部署压力**：在实时控制（10–20 Hz）约束下，CoT 的长度直接影响可行性。

## Related Concepts

- [[VLA-Architecture|VLA Architecture]] — CoT 作为生成/推理引擎的中间输出
- [[Vision-Language-Action|Vision-Language-Action (VLA)]] — CoT 在具身智能中的应用范式
- [[02_AI/Cognitive-Architecture/Mode-1-Mode-2-Reasoning|Mode 1 / Mode 2 Reasoning]] — 快速直觉与慢速推理的对比

## Papers

- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 将 CoT 描述为 VLA 推理引擎可能生成的中间输出
