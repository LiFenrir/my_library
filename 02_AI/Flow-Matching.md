---
title: Flow Matching
description: 通过回归概率密度向量场来训练连续生成模型的方法，常用于机器人动作生成
tags:
  - ai
  - generative-model
  - flow-matching
  - robot-learning
created: 2026-07-28
---

# Flow Matching

Flow Matching 是一种**连续生成模型**训练方法，通过直接回归从一个分布到另一个分布的概率路径速度场来学习生成过程。

## Core Idea

给定源分布（如标准高斯噪声）和目标分布（如数据分布），构造一条连接两者的概率路径。模型学习该路径上每个点的速度场，从而可以通过常微分方程（ODE）将噪声变换为样本。

## Why It Works

相比扩散模型需要对离散时间步建模，Flow Matching 直接在连续时间上回归向量场，训练更稳定、采样更灵活。

## 与 Diffusion 的关系

Flow Matching 与扩散模型（Diffusion）在数学上等价：通过适当选择噪声调度，DDPM/Score-based 模型可转化为 Flow Matching 形式。Flow Matching 的优势在于：

- 可以定义更灵活、更直的路径（如最优传输路径）
- 训练和采样公式更简洁
- 常与 Classifier-Free Guidance (CFG) 结合控制生成条件

## 优缺点

- **优点**：连续生成、ODE 采样步数可少、路径设计灵活、易于条件控制
- **局限**：对复杂多峰分布仍需要足够模型容量；采样质量依赖数值积分精度

## Key Components

- **概率路径** $p_t$：从 $p_0$（噪声）到 $p_1$（数据）的插值
- **向量场** $u_t$：描述样本在连续时间上的演化速度
- **条件流匹配损失**：
  $$
  \mathcal{L}_{\text{CFM}} = \mathbb{E}_{t, x_t} \| v_\theta(x_t, t) - u_t(x_t) \|^2
  $$

## In Robotics

在机器人策略中，Flow Matching 常被用作动作专家（Action Expert）的生成目标，以建模机器人动作的多模态分布。

## Related Concepts

- [[Classifier-Free-Guidance|Classifier-Free Guidance]] — 引导生成朝向条件样本
- [[01_Fundamentals/ML/diffusion-model|Diffusion Model]] — 另一种基于分数匹配的生成方法
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 将 Flow Matching 用于动作生成的 VLA 框架
- [[04_Embodied-AI/VLA/Flow-based-VLA|Flow-based VLA]] — 基于流匹配的 VLA 实例

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 使用 Flow Matching 动作专家生成 50 步动作块

## Conditional Flow Matching (CFM)

CFM 是 Flow Matching 的条件化形式，常用于世界-动作模型（WAM）中生成未来观测或动作。

### ODE 流形式

给定目标生成状态 $x$（如未来帧 $o_{t+1}$ 或动作 $a_t$）和源噪声 $\epsilon \sim \mathcal{N}(0, I)$，条件向量场 $v_\phi(x^{(s)}, s \mid c)$ 描述从噪声到数据的演化：

$$
\frac{d x^{(s)}}{d s} = v_\phi(x^{(s)}, s \mid c), \quad x^{(0)} = \epsilon \sim \mathcal{N}(0, I)
$$

其中 $s \in [0, 1]$ 为连续流时间，$c = (o_{\leq t}, a_{<t}, l)$ 为历史观测、动作和语言指令构成的条件上下文。

### 最优传输路径

按最优传输构造线性插值：

$$
x^{(s)} = (1 - s)\epsilon + s \cdot x
$$

其速度为恒定向量：

$$
\dot{x}^{(s)} = x - \epsilon
$$

### 训练目标

神经网络通过回归条件向量场来拟合该速度：

$$
\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{s, \epsilon, x, c} \left[ \| v_\phi(x^{(s)}, s \mid c) - \dot{x}^{(s)} \|^2 \right]
$$

### 推理

从随机噪声 $\epsilon$ 出发，使用 ODE 求解器（如 Euler）迭代积分学习到的向量场，逐步去噪得到预测状态。

### 在 WAM 中的瓶颈

直接以原始像素 $x = o_{t+1}$ 为目标会迫使流匹配拟合大量任务无关的高频纹理；同时条件上下文 $c$ 随时间线性增长，导致 KV cache 内存按 $\mathcal{O}(T)$ 扩张。Causal Latent World Model 通过将目标转移到 DINOv3 语义空间并用 TTT Memory 替换 KV cache 来缓解这两个问题。

### Related Concepts

- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — 使用 CFM 作为生成主干的机器人策略框架
- [[04_Embodied-AI/World-Model/causal-latent-world-model|Causal Latent World Model]] — 在语义空间中使用 CFM 的世界模型

## 实例：Fast-WAM 的联合流匹配目标

Fast-WAM 将流匹配同时用于动作生成与未来视频 latent 建模。对目标变量 $y$（动作块 $a_{1:H}$ 或未来视频 latent $z_{1:T}$），采样高斯噪声 $\epsilon \sim \mathcal{N}(0,I)$ 与时间步 $t \in (0,1)$，构造插值样本：
$$
y_t = (1-t)y + t\epsilon
$$

模型学习预测速度场：
$$
\mathcal{L}_{\text{FM}}(y) = \mathbb{E}_{y,\epsilon,t} \left[ \| f_\theta(y_t, t, o, l) - (\epsilon - y) \|_2^2 \right]
$$

整体训练目标为动作损失与视频协同训练损失的加和：
$$
\mathcal{L} = \mathcal{L}_{\text{act}} + \lambda \mathcal{L}_{\text{vid}}
$$
其中
- $\mathcal{L}_{\text{act}} = \mathcal{L}_{\text{FM}}(a_{1:H})$
- $\mathcal{L}_{\text{vid}} = \mathcal{L}_{\text{FM}}(z_{1:T})$
- $\lambda$ 平衡动作学习与视频建模

## 来源

- [[05_Papers/articles/pi0-7|π0.7]] — 使用 Flow Matching 动作专家生成 50 步动作块
- [[05_Papers/articles/fast-wam|Fast-WAM: Do World Action Models Need Test-time Future Imagination?]]
- Yaron Lipman et al., *Flow Matching for Generative Modeling*, arXiv:2210.02747

## 补充：来自 [[02_AI/Flow-Matching|flow-matching（已合并）]]

### Conditional Flow Matching for Video Generation

在视频生成中，flow matching 被扩展为**条件流匹配**：给定文本 $c$ 或初始图像作为条件，模型学习从噪声到视频 latent 序列的向量场。

视频帧先由预训练视频 VAE 编码为隐变量 $z_t = E(o_t)$，生成目标为 latent 帧序列 $\mathbf{z} = \{z_1, \dots, z_T\}$。条件流匹配学习目标为：

$$
v_\theta(\mathbf{z}^{(s)}, s \mid c) = \frac{d}{ds} \mathbf{z}^{(s)}
$$

其中 $s \in [0, 1]$ 为 flow time，$\mathbf{z}^{(0)} = \boldsymbol{\epsilon} \sim \mathcal{N}(0, I)$，最终 latent 视频 $\bar{\mathbf{z}}^{(1)}$ 经 VAE 解码回像素空间。

这种条件化框架支持从文本描述或种子图像灵活生成视频，是视频世界模型的基础训练目标（见 [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]]）。
