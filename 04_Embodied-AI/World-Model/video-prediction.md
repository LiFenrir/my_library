---
title: "Video Prediction"
description: "基于历史观测生成未来视频帧的生成模型任务"
tags: [concept, embodied-ai, world-model, video-generation]
created: 2026-07-29
---

# Video Prediction

**核心定义**：Video Prediction 是根据过去视频帧（以及可选动作、文本条件）生成未来帧的生成建模任务。它是世界模型学习视觉动力学的基础能力。

## 常见方法

| 方法 | 特点 |
|------|------|
| VAE + RNN | 将每帧压缩为潜在变量，用 RNN 建模时序 |
| Autoregressive Models | 逐帧或逐 chunk 生成，因果一致 |
| Diffusion/Flow Models | 在潜在空间进行迭代去噪生成 |
| Video Diffusion Transformers | 用 transformer 统一空间-时间建模 |

## 在机器人中的作用

- 作为世界模型预测环境演化
- 生成子目标图像供 VLA 使用
- 用于动作规划（predictive control）
- 支持 long-horizon 任务的时间一致性

## 优缺点

- **优点**：直观、可解释、可利用大规模视频数据预训练
- **缺点/局限**：开环预测误差会复合；长程一致性难保证；计算成本高

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/World-Model|World Model]] — Video Prediction 是世界模型的视觉形式
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 强调因果一致的视频预测
- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]] — 视频预测在 VLA 中的应用

## 训练时 vs 测试时的角色区分

Fast-WAM 的研究指出，视频预测在 WAM 中的价值可能主要体现为**训练时的表示学习信号**，而非测试时显式生成未来帧：

- **训练时**：视频预测目标迫使模型学习物理动态、物体交互与时间结构，从而得到更好的动作条件表示
- **测试时**：显式未来生成提供额外的前瞻（foresight），但可能并非性能的主要来源；移除测试时想象可显著降低延迟，同时保持竞争力

这一区分对应于两个因素的解耦：
1. 视频建模目标（video co-training objective）
2. 测试时未来想象（test-time future imagination）

## 来源

- [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]]，第 2.2、3.2 节
- [[05_Papers/articles/world-models|World Models]]，第 2.2 节
- [[05_Papers/articles/fast-wam|Fast-WAM: Do World Action Models Need Test-time Future Imagination?]]
