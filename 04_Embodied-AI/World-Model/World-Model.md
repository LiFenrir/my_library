---
title: "World Model"
description: "智能体通过无监督学习构建的压缩时空环境模型，可用于特征提取、未来预测与在虚拟‘梦境’中训练策略。"
tags: [concept, embodied-ai, world-model, latent-dynamics, model-based-rl, video-prediction]
created: 2026-07-28
---

# World Model

World Model 是智能体从其经验中无监督学习得到的对环境时空规律的压缩表示。它把高维观测序列抽象为低维潜在状态，并预测未来状态，使智能体能够基于内部模型快速决策，甚至完全在模型生成的“梦境”中训练策略。

## 为什么需要 World Model

- 真实环境通常具有高维像素输入和复杂的长期时间依赖，传统无模型 RL 受信用分配问题限制，只能使用较小的网络。
- 把“理解世界”与“决策控制”解耦：让大容量网络学习环境表征与预测，再用极小的控制器完成策略优化。
- 内部模型能够替代真实环境进行大量低成本 rollout，减少昂贵仿真或真实交互。

## 核心结构（V-M-C）

受认知系统启发，World Model 由三个模块紧密协作：

- **Vision (V)**：把高维观测（如图像帧）压缩为低维潜在向量 $z_t$。
- **Memory (M)**：基于历史信息预测未来潜在向量 $z_{t+1}$ 的分布，即环境的动力学模型。
- **Controller (C)**：根据当前表征 $z_t$ 与记忆隐藏状态 $h_t$ 决定动作 $a_t$。

这种分工让控制器保持极简（如单层线性模型），而世界模型承载大部分表达能力。

## 关键机制

### 1. 观测压缩（VAE）

使用 [[Variational-Autoencoder|VAE]] 把每一帧图像编码为低维潜在向量 $z$，解码器可重建原始帧。潜在空间使 M 模块不必直接处理高维像素。

### 2. 潜在动力学（MDN-RNN）

M 模型通常是一个带 [[Mixture-Density-Network|MDN]] 输出的循环网络，建模条件分布：

$$
P(z_{t+1} \mid a_t, z_t, h_t)
$$

由于环境具有随机性，MDN 用高斯混合分布刻画多模态未来，而非确定性点估计。采样时可通过温度参数 $\tau$ 调节模型不确定性。

### 3. 控制器

控制器将 $z_t$ 与 $h_t$ 拼接后直接映射为动作：

$$
a_t = W_c [z_t \ h_t] + b_c
$$

在 World Models 工作中，C 使用 [[Evolution-Strategies|CMA-ES]] 等进化策略优化，因为参数空间小且只需要最终累计奖励。

## 在“梦境”中训练策略

若 World Model 足够准确，可把它封装为与真实环境接口一致的虚拟环境，让智能体完全在潜在空间中训练。训练好的策略可迁移回真实环境。为避免智能体利用模型缺陷，可通过提高采样温度 $\tau$ 增加梦境难度，使策略更鲁棒。

## 迭代训练

对于更复杂的任务，可采用迭代流程：

1. 用当前策略在真实环境中收集 rollout 数据。
2. 用新数据更新 M，同时用 M 中的虚拟环境优化 C。
3. 重复直到任务解决。

这与好奇心、内在动机等探索机制结合，可让智能体主动收集能改善世界模型的数据。

## 在机器人中的应用

- 子目标图像生成（如 π0.7 中用于 VLA 提示，见 [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]]）
- 视频预测用于动作规划
- 世界模型作为策略学习的仿真器
- 因果世界建模用于长程操作（见 [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]]）

## 优势与局限

- 优势：控制器极小、训练高效；可在潜在空间大量 rollouts；把高维像素控制问题转化为低维潜在空间控制问题。
- 局限：VAE 可能编码任务无关细节；模型容量有限、存在灾难性遗忘；智能体可能找到对抗策略利用模型误差；迁移性能依赖模型在分布外的泛化能力；模型误差会复合（compounding error）。

## 与其他概念的关系

- [[Model-Based-Reinforcement-Learning|Model-Based RL]] — World Model 是 MBRL 的一种实现形式。
- [[Variational-Autoencoder|VAE]] — 用于观测压缩的生成模型。
- [[Mixture-Density-Network|MDN]] — 用于建模多模态潜在动力学的输出层。
- [[Evolution-Strategies|Evolution Strategies]] — 用于优化小控制器的黑箱优化方法。
- [[04_Embodied-AI/Sim2Real/index|Sim2Real]] — 在虚拟/仿真环境中学到的策略迁移到真实世界。
- [[04_Embodied-AI/World-Model/video-prediction|Video Prediction]] — World Model 的视觉预测形式。
- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]] — 世界模型在 VLA 中的应用。

## 补充：来自 [[05_Papers/articles/world-models|World Models]]

### 在梦境中剥削世界模型

当控制器 $C$ 完全在学习到的世界模型中训练时，它可能发现**对抗策略**（adversarial policy）来操纵 $M$ 的缺陷而非学会真实任务：

- $C$ 能访问 $M$ 的全部隐藏状态，相当于能“看到”游戏引擎内部，而非仅看到玩家视角的观测。
- $C$ 可能找到让怪物停止发射火球、或让已发射火球消失的轨迹，因为这些状态虽在 $M$ 的分布内看起来合理，却不符合真实环境规律。
- 这类策略在梦境中表现优异，迁移到真实环境后失败，通常是因为它访问了 $M$ 训练分布之外的状态。

缓解方法：

- 使用概率模型（如 MDN-RNN）而非确定性动力学模型，增加 $M$ 内在的随机性。
- 通过提高采样温度 $\tau$ 让梦境更困难、更多样，迫使 $C$ 学习对模型误差更鲁棒的策略。
- 结合模型自由方法在真实环境中对策略进行微调（如 Nagabandi et al., 2017）。

### 温度参数的双重作用

$\tau$ 在 World Models 中不仅是控制样本多样性的参数，也是调节**梦境难度**的旋钮：

- 低 $\tau$：梦境接近确定性，$C$ 容易过拟合到 $M$ 的特定缺陷。
- 高 $\tau$：梦境更随机，抑制对抗策略，但过高会使任务过难、策略无法学习。

最优 $\tau$ 需要在真实环境迁移性能上调参。

### VAE 的任务无关特征问题

将 VAE 作为独立感知模块训练存在局限：无监督重建目标不知道哪些视觉细节对下游任务重要。

- 在 Doom 环境中，VAE 可能精确重建无关的砖墙纹理，却忽略任务相关的路面标记。
- 若将 VAE 与 $M$ 的奖励预测联合训练，可促使潜在空间关注任务相关区域，但会牺牲跨任务复用能力。

### 模型容量与灾难性遗忘

以 LSTM 为基础的 $M$ 容量有限，难以在迭代训练过程中记住所有历史经验。与能够长期 Consolidate 记忆的人脑不同，神经网络容易遭受灾难性遗忘。未来方向包括使用更大容量的网络架构或外部记忆模块。

### 与 Learning to Think 的关系

World Models 中 $C$ 依赖 $M$ 逐步预测未来，属于较早期的 C–M 系统形式。更一般的 [[Learning-to-Think|Learning to Think]] 框架允许 $C$ 把 $M$ 的权重子程序当作任意计算资源使用，支持分层规划、抽象推理，并在 $M$ 不可靠时选择忽略它。

## 来源

- [[05_Papers/articles/world-models|World Models]]
- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]，LeCun，2022

## 补充：来自 [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]

LeCun 从认知架构角度提出另一种世界模型路线：不再生成像素，而是在表示空间中做预测，核心架构为 [[Joint-Embedding-Predictive-Architecture|JEPA]] 与 [[Hierarchical-JEPA|H-JEPA]]。

### 与 V-M-C 路线的关键区别

| 维度 | Ha & Schmidhuber 路线 | LeCun 路线 |
|------|------------------------|------------|
| 预测空间 | 像素 / 原始观测 | 抽象表示 |
| 核心架构 | VAE + MDN-RNN | JEPA / H-JEPA |
| 多模态未来 | MDN 混合分布 | 编码器不变性 + 隐变量 |
| 训练方式 | 重建 + 预测 | 非对比 SSL（如 VICReg） |
| 抽象层次 | 单一潜在空间 | 多层抽象、多时间尺度 |

### LeCun 路线的优势

- 不必预测不可预测的细节（如树叶抖动、水面波纹）。
- 可学习层次化抽象概念（物体、恒存性、直观物理）。
- 更适合作为 Mode-2 推理与分层规划的前向模型。

### 相关概念

- [[Joint-Embedding-Predictive-Architecture|JEPA]] — 非生成式预测架构。
- [[Hierarchical-JEPA|H-JEPA]] — 分层世界模型。
- [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|[[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]] — 包含世界模型的完整认知架构。
