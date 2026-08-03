---
title: "Vision-Language-Action Model (VLA)"
description: "基于预训练视觉-语言模型 backbone、通过生成式动作头输出机器人动作的多模态策略模型通用定义与训练目标。"
tags: [concept, ai, multimodal, vlm, robot-policy]
created: 2026-07-28
---

# Vision-Language-Action Model (VLA)

**核心定义**：VLA 是从预训练视觉-语言模型（VLM）backbone 出发、适配到机器人控制任务的多模态策略模型。它接收视觉观测与语言指令等上下文，直接生成底层机器人动作（关节或末端执行器命令）。

## 原理

- **输入表示**：训练数据集 $\mathcal{D}$ 由机器人轨迹组成，每条轨迹是观测 $\mathbf{o}_t$ 与动作 $\mathbf{a}_t$ 的序列。
  - 观测：$\mathbf{o}_t = [\mathbf{I}_t^1, \ldots, \mathbf{I}_t^n, \mathbf{q}_t]$，包含 $n$ 个相机图像与机器人关节状态（本体感知）。
  - 动作：$\mathbf{a}_t$ 为关节或末端执行器命令。
- **动作块预测**：模型基于近期观测历史 $\mathbf{o}_{t-T:t}$，预测未来一段动作序列（action chunk）$\mathbf{a}_{t:t+H}$。实际执行时通常只使用其中前 $\hat{H} < H$ 步。
- **动作专家（action expert）**：一个较小的 transformer， attending 到 VLM backbone 的激活上，负责快速推理并生成连续动作。它通常采用 [[flow-matching|Flow Matching]] 或 [[diffusion-model|Diffusion]] 目标，以捕捉机器人动作的多模态分布。
- **知识隔离（Knowledge Insulation, KI）**：VLM backbone 通过离散 token 的监督任务（如 FAST tokens）训练，动作专家的梯度不回流到 VLM backbone，从而保持视觉-语言表示稳定。
- **上下文条件**：训练时每个样本都带有一个上下文 $\mathcal{C}_t$。最简形式是人工标注的语言指令 $\ell_t$，即 $\mathcal{C}_t = (\ell_t)$；也可以扩展为子任务指令、目标图像、元数据等多模态信息。

## 训练目标

VLA 的学习目标是对条件动作分布的近似对数似然：

$$
\max_{\theta} \mathbb{E}_{\mathcal{D}} \left[ \log \pi_{\theta}\left(\mathbf{a}_{t:t+H} \mid \mathbf{o}_{t-T:t}, \mathcal{C}_t\right) \right]
$$

当 action expert 使用 Flow Matching 时，优化的是该对数似然的近似下界，而非闭式对数似然。

## 优缺点

- **优点**：可以直接利用预训练 VLM 的视觉-语言理解能力；动作专家通过生成式目标建模多峰动作分布；语言/视觉上下文提供了灵活的任务指定方式。
- **局限/适用条件**：本质上仍是条件模仿学习，对数据分布敏感；高质量、多策略数据需要额外的上下文标注（如速度、质量、子目标图像）来解歧；推理延迟和动作块长度需要在实时控制中权衡。

## 与其他概念的关系

- [[vision-language-model|Vision-Language Model (VLM)]] — VLA 的视觉-语言 backbone 来源。
- [[flow-matching|Flow Matching]] / [[diffusion-model|Diffusion Model]] — action expert 常用的连续动作生成目标。
- [[robot-imitation-learning|Robot Imitation Learning]] — VLA 训练通常属于大规模条件行为克隆。
- [[04_Embodied-AI/index|Embodied AI]] — VLA 是具身智能中机器人策略的一类重要实现形式。

## 来源

- [[05_Papers/articles/pi0-7|π0.7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities]]，第 III 节 "Flow-based Vision-Language-Action Models"。
