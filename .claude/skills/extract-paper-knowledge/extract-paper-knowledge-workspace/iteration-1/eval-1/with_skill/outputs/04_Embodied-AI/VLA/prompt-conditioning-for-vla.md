---
title: "Prompt Conditioning for VLA"
description: "通过多模态、细粒度上下文提示来消除 VLA 训练数据中的歧义，实现数据多样性利用与测试时策略控制。"
tags: [concept, embodied-ai, vla, prompting, multimodal, robot-policy]
created: 2026-07-28
---

# Prompt Conditioning for VLA

核心定义：**Prompt Conditioning for VLA** 是指在 Vision-Language-Action 模型的上下文 $\mathcal{C}_t$ 中，不仅给出“做什么”的高层语言指令，还提供“怎么做”的多模态细节，从而把异质、多策略、多质量的数据转化为可区分的条件分布。

## 原理

在异质机器人数据中，同一语言指令可能对应多种执行策略和质量水平。简单地对所有数据求平均会导致策略退化。通过在训练时为每条轨迹附加丰富的上下文标签，并让模型在测试时通过相同或部分上下文进行条件采样，可以把一个“平均分布”拆分为多个高质量、可控的条件分布。

训练时每个提示组件随机 dropout，使模型在测试时能接受任意子集。

## 上下文组件

1. **任务语言指令** $\ell_t$：高层目标，如 "clean the kitchen"。
2. **子任务指令** $\hat{\ell}_t$：下一语义子任务，如 "open the fridge door"。可由高层策略或人类实时生成，也支持语言 coaching。
3. **子目标图像** $\mathbf{g}_t$：多视角近未来目标图像，补充语言难以表达的空间与外观细节。
4. **Episode Metadata** $m$：描述轨迹质量与策略的属性。
   - Overall speed：轨迹长度（离散化到时间步区间）。
   - Overall quality：1–5 的质量评分。
   - Mistake：该片段是否包含错误。
5. **Control Mode** $c$：动作空间标识，如 joint / end-effector。

## 测试时配置

- 元数据通常固定为“高质量、高速度、无错误”，以激发最佳表现。
- 子目标图像按时间或子任务变化异步刷新。
- 可对任意上下文组件使用 classifier-free guidance（CFG），引导生成动作偏向特定属性（如更高速度）。

## 优缺点

- 优点：
  - 能把失败、次优、自主回滚等低质量数据转化为可用训练信号。
  - 支持测试时零样本策略切换（速度、质量、控制模式）。
  - 子目标图像引入视觉类比能力，有利于跨本体迁移。
- 缺点 / 局限：
  - 需要为训练数据标注细粒度上下文，标注成本高。
  - 各组件 dropout 比例和 CFG 权重需要调优。
  - 提示设计不当可能放大训练数据中的偏见。

## 与其他概念的关系

- [[vla-architecture|VLA Architecture]] — prompt conditioning 作用于 VLA 的上下文输入。
- [[knowledge-insulation|Knowledge Insulation]] — 常与 prompt conditioning 在同一训练 pipeline 中使用。
- [[02_AI/Flow-Matching-action-expert|Flow Matching Action Expert]] — 在丰富条件下生成动作块。

## 来源

- [[05_Papers/articles/pi0-7|π0.7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities]] — Sec. V, Sec. VII
