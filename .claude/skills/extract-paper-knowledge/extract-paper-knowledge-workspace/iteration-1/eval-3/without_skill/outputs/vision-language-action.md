---
title: "Vision-Language-Action (VLA) 模型"
description: "从 pi0.7 论文提取的 VLA 通用定义、训练目标与架构要素"
tags: [vla, embodied-ai, robot-learning, multimodal, concept]
created: 2026-07-28
source: "05_Papers/articles/pi0-7.md"
---

# Vision-Language-Action (VLA) 模型

VLA 是从预训练视觉-语言模型（VLM）出发、适配到机器人控制的多模态策略模型。

## 通用定义

- 输入：历史观测序列 $\mathbf{o}_{t-T:t}$ 与上下文提示 $\mathcal{C}_t$。
- 输出：未来动作块（action chunk）$\mathbf{a}_{t:t+H}$。
- 观测 $\mathbf{o}_t = [\mathbf{I}_t^1, \ldots, \mathbf{I}_t^n, \mathbf{q}_t]$ 包含多视角图像与机器人本体状态。
- 动作 $\mathbf{a}_t$ 为关节或末端执行器指令。
- 上下文 $\mathcal{C}_t$ 传统上仅为语言指令 $\ell_t$，但可扩展为子任务指令、子目标图像、episode 元数据、控制模式等。

## 训练目标

最大化动作块在观测与上下文条件下的近似对数似然：

$$
\max_{\theta} \mathbb{E}_{\mathcal{D}} \left[ \log \pi_{\theta}\left(\mathbf{a}_{t:t+H} \mid \mathbf{o}_{t-T:t}, \mathcal{C}_t\right) \right]
$$

动作专家通常使用 flow matching 或扩散目标，以捕捉机器人动作的多模态分布；VLM backbone 则通过离散交叉熵等更稳定的损失进行监督。

## 关键架构组件

1. **VLM backbone**：提供视觉-语言理解与表征，常使用 Gemma、PALM-E 等预训练模型初始化。
2. **Action expert**：轻量 transformer，接收 VLM 激活并预测连续动作，典型大小 860M 参数。
3. **Flow matching / diffusion**：对动作块进行去噪生成，建模多模态动作分布。
4. **Knowledge insulation (KI)**：action expert 可 attend VLM 全部激活，但梯度不回传 VLM，保持 VLM 训练稳定。
5. **上下文 / prompt**：语言指令、子任务、子目标图像、episode 元数据、控制模式等，训练时随机 dropout 以支持测试时灵活组合。

## 与相关概念的关系

- 属于 [[04_Embodied-AI/index|具身智能]] 中的 [[04_Embodied-AI/VLA/index|VLA]] 子领域。
- 底层依赖 [[03_Robotics/index|机器人底层技术]]（控制、感知、硬件）。
- 与 [[02_AI/index|通用 AI]] 的 VLM、LLM 有继承关系，但 VLA 必须绑定物理 embodiment 与动作输出。
