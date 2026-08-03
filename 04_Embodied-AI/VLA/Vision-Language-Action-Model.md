---
title: Vision-Language-Action Model
description: 将视觉语言模型与机器人动作生成结合，直接输出低层控制信号的具身智能模型范式
tags:
  - embodied-ai
  - vla
  - robotics
  - foundation-model
created: 2026-07-28
---

# Vision-Language-Action Model

Vision-Language-Action Model（VLA）是一类**直接根据视觉和语言指令生成机器人动作**的具身智能基础模型。

## Core Idea

将预训练的 Vision-Language Model（VLM）扩展为能够输出机器人控制信号的策略模型。输入为图像观察和语言指令，输出为关节或末端执行器动作。

## Typical Architecture

- **VLM Backbone**：处理视觉和语言输入，提供多模态表示
- **Action Head / Action Expert**：基于 VLM 表示生成动作
- **Observation Encoder**：将相机图像和本体感受编码为 token

## 原理（π0.7 形式化）

- **输入表示**：训练数据集 $\mathcal{D}$ 由机器人轨迹组成，每条轨迹是观测 $\mathbf{o}_t$ 与动作 $\mathbf{a}_t$ 的序列。
  - 观测：$\mathbf{o}_t = [\mathbf{I}_t^1, \ldots, \mathbf{I}_t^n, \mathbf{q}_t]$，包含 $n$ 个相机图像与机器人关节状态（本体感知）。
  - 动作：$\mathbf{a}_t$ 为关节或末端执行器命令。
- **动作块预测**：模型基于近期观测历史 $\mathbf{o}_{t-T:t}$，预测未来一段动作序列（action chunk）$\mathbf{a}_{t:t+H}$，实际执行时通常只使用其中前 $\hat{H} < H$ 步（见 [[04_Embodied-AI/VLA/Action-Chunking|Action Chunking]]）。
- **动作专家（action expert）**：一个较小的 transformer，attending 到 VLM backbone 的激活上，负责快速推理并生成连续动作。通常采用 [[02_AI/Flow-Matching|Flow Matching]] 或 [[01_Fundamentals/ML/diffusion-model|Diffusion]] 目标，以捕捉机器人动作的多模态分布。
- **知识隔离（Knowledge Insulation, KI）**：VLM backbone 通过离散 token 的监督任务（如 FAST tokens）训练，动作专家的梯度不回流到 VLM backbone，保持视觉-语言表示稳定（见 [[04_Embodied-AI/VLA/Knowledge-Insulation|Knowledge Insulation]]）。
- **上下文条件**：训练时每个样本都带有一个上下文 $\mathcal{C}_t$。最简形式是人工标注的语言指令 $\ell_t$；也可以扩展为子任务指令、目标图像、元数据等多模态信息。

## Training Objective

通常最大化动作序列的对数似然：

$$
\max_\theta \mathbb{E}_{\mathcal{D}} \left[ \log \pi_\theta(a_{t:t+H} \mid o_{t-T:t}, \mathcal{C}_t) \right]
$$

其中 $\mathcal{C}_t$ 为上下文提示，$H$ 为动作块长度。当 action expert 使用 Flow Matching 时，优化的是该对数似然的近似下界，而非闭式对数似然。

## Key Challenges

- 动作多模态性：同一指令可对应多种执行方式
- 跨 embodiment 泛化：不同机器人形态共享策略
- 长程任务与实时推理的平衡

## 优缺点

- **优点**：可直接利用预训练 VLM 的视觉-语言理解能力；动作专家通过生成式目标建模多峰动作分布；语言/视觉上下文提供灵活的任务指定方式。
- **局限**：本质上仍是条件模仿学习，对数据分布敏感；高质量、多策略数据需要额外的上下文标注（如速度、质量、子目标图像）来解歧；推理延迟和动作块长度需要在实时控制中权衡。

## Related Concepts

- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — VLA 的感知与语言 backbone
- [[04_Embodied-AI/VLA/Action-Expert|Action Expert]] — 负责动作生成的子模块
- [[04_Embodied-AI/VLA/Flow-based-VLA|Flow-based VLA]] — 使用流匹配动作生成的 VLA
- [[04_Embodied-AI/VLA/Diverse-Prompting-for-VLA|Diverse Prompting for VLA]] — 通过丰富提示增强 VLA 能力
- [[04_Embodied-AI/VLA/Cross-embodiment-Generalization|Cross-embodiment Generalization]] — VLA 的跨机器人泛化
- [[01_Fundamentals/ML/Imitation-Learning|Imitation Learning]] — VLA 训练通常属于大规模条件行为克隆
- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — 与 VLA 并行的机器人策略范式

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 通过多样化提示实现可引导的通用 VLA
- [[RT-2]] — 将 VLM 知识迁移到机器人控制
- [[OpenVLA]] — 开源 VLA 代表

## 补充：来自 [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]]

### 表示纠缠（Representation Entanglement）

传统 VLA 采用前馈范式 $\pi(a_t \mid o_t)$，要求单一网络同时学习：

- 视觉场景理解
- 物理动力学
- 运动控制

这种**表示纠缠**导致：

- 样本效率低下：异质知识被压缩到同一表示空间；
- 泛化能力受限：模型容易依赖模式匹配而非对物理动力学的原理性理解；
- 难以解耦视觉推理与动作预测。

世界模型视角通过显式建模环境演化 $p(o_{t+1} \mid o_{\leq t}, a_{\leq t})$ 来缓解这一问题，将视觉动态学习与动作解码分离。
