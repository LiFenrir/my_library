---
title: "Flow Matching Action Expert"
description: "用流匹配（Flow Matching）生成连续动作序列的通用生成模型方法，常用于 VLA 等需要建模多峰动作分布的场景。"
tags: [concept, ai, generative-model, flow-matching, vla, action-generation]
created: 2026-07-28
---

# Flow Matching Action Expert

核心定义：在机器人或连续控制场景中，**action expert** 是一个轻量 transformer，负责在 VLM/多模态骨干网络提供的上下文表征基础上生成未来动作序列；当该专家使用 **flow matching** 目标训练时，即称为 flow matching action expert。它把动作生成看作从噪声到动作分布的连续概率流建模，能够自然捕捉同一状态下多种合理动作的多峰分布。

## 原理

1. **动作块（action chunk）预测**：模型不预测单步动作，而是预测一段未来动作轨迹 $\mathbf{a}_{t:t+H}$，对应一个动作块。动作块可以提高时间一致性和执行效率。
2. **条件流匹配**：给定观测历史 $\mathbf{o}_{t-T:t}$ 和上下文 $\mathcal{C}_t$，动作专家学习条件向量场，将简单先验（通常是高斯噪声）变换为目标动作分布。训练目标为条件流匹配损失 $\mathcal{L}_{\mathrm{CFM}}$。
3. **与骨干解耦**：action expert 通常比 VLM 骨干小得多（例如 860M vs 4B），只通过 cross-attention 读取骨干激活，从而在保证推理速度的同时保留大模型的语义理解能力。
4. **多步去噪推理**：测试时通过少量去噪步（如 5 步）从噪声采样出动作块，兼顾质量与延迟。

## 公式

VLA 的训练目标可写成近似对数似然：

$$
\max_{\theta} \mathbb{E}_{\mathcal{D}} \left[ \log \pi_{\theta}\left(\mathbf{a}_{t:t+H} \mid \mathbf{o}_{t-T:t}, \mathcal{C}_t\right) \right]
$$

其中 flow matching action expert 实际优化的是该对数似然的近似下界，而非闭式解。

- $\mathbf{o}_{t-T:t}$：观测历史
- $\mathbf{a}_{t:t+H}$：未来 $H$ 步动作块
- $\mathcal{C}_t$：包含语言指令、子任务、子目标图像、元数据等多模态上下文
- $\pi_\theta$：由 VLM 骨干 + action expert 组成的策略

## 优缺点

- 优点：
  - 能建模连续动作的多峰分布，避免平均化不同策略。
  - 去噪步数可控，便于在质量与推理速度之间权衡。
  - action expert 与语义骨干解耦，利于分别优化和部署。
- 缺点 / 局限：
  - 需要设计合适的条件注入（如 timestep embedding、adaptive RMSNorm）。
  - 多峰分布能力高度依赖训练数据质量和条件信息的丰富程度。
  - 对长动作块的误差累积敏感。

## 与其他概念的关系

- [[vla-architecture|VLA Architecture]] — action expert 是 VLA 的动作生成头。
- [[prompt-conditioning-for-vla|Prompt Conditioning for VLA]] — 上下文 $\mathcal{C}_t$ 的质量直接影响 flow matching action expert 的条件生成效果。
- [[knowledge-insulation|Knowledge Insulation]] — 常与 flow matching action expert 配合使用，防止动作梯度破坏 VLM 骨干。

## 来源

- [[05_Papers/articles/pi0-7|π0.7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities]] — Sec. III
