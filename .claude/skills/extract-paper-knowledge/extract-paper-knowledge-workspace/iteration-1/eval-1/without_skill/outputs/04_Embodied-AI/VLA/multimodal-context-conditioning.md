---
title: "VLA 的多模态上下文条件"
description: "通过扩展 prompt 消解数据歧义，使 VLA 能利用多样化、混合质量的数据，并支持测试时灵活引导。"
tags: [embodied-ai, vla, prompting, context-conditioning]
created: 2026-07-28
---

# VLA 的多模态上下文条件

仅靠语言指令不足以描述“怎么做”，因此 VLA 可在 prompt 中加入多种上下文信号，把训练数据中的歧义模式区分开。

## Prompt 组成

1. **任务指令** $\ell_t$：总体语言目标，如“clean the kitchen”。
2. **子任务指令** $\hat{\ell}_t$：下一语义步骤，如“open the fridge door”。可由高层策略或人类教练提供。
3. **子目标图像** $\mathbf{g}_t$：近未来期望视觉状态，由世界模型生成；多视角同时约束环境与手臂姿态。
4. **Episode Metadata**：
   - **Overall speed**：episode 长度分桶，刻画速度/效率模式。
   - **Overall quality**：1–5 分质量评分。
   - **Mistake label**：该段是否包含错误。
5. **Control Mode**：`joint` 或 `ee`，指定动作空间。

## 训练与测试机制

- **随机 Dropout**：训练时各 prompt 组件按概率 dropout，使模型在测试时可接受任意子集。
- **Classifier-Free Guidance**：推理时对 metadata 等做 CFG，引导模型偏向高速、高质量、无错误的行为。
- **测试时默认 metadata**：speed 取任务 15th 百分位，quality=5，mistake=false。

## 为什么有效

- 区分数据中的不同质量/策略模式，避免简单平均。
- 允许使用失败片段、次优自主 rollouts、人类视频等非标准数据源。
- 支持用语言或图像“ Coaching ”新任务，无需重新采集动作数据。

相关：
- [[04_Embodied-AI/VLA/VLA-architecture|VLA 架构要素]] — prompt 如何接入模型
- [[04_Embodied-AI/World-Model/subgoal-image-world-model|子目标图像世界模型]] — 子目标图像生成
- [[04_Embodied-AI/VLA/learning-from-mixed-quality-data|利用 episode metadata 学习混合质量数据]] — metadata 的数据缩放价值
- [[05_Papers/articles/pi0-7|pi0.7 论文笔记]]
