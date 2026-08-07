---
title: "Causal World Model"
description: "通过因果注意力保持时间一致性，将视觉动力学预测与动作推断统一在自回归序列中的世界模型"
aliases:
  - Causal Latent World Model
  - CLWM
tags: [concept, embodied-ai, world-model, causal-reasoning]
created: 2026-07-29
---

# Causal World Model

一类尊重物理世界因果结构的世界模型：当前状态仅依赖于过去，未来不能影响现在。它通过因果注意力掩码和自回归生成，将视觉动力学预测与动作推断统一在单一序列中。

## 核心问题

传统视频世界模型或 chunk-based 扩散方法存在三个问题：

1. **Reactivity Gap**：开环生成长序列，无法纳入实时反馈
2. **Limited Long-term Memory**：chunk 独立生成，缺乏跨 chunk 的持久记忆
3. **Causality Violation**：chunk 内双向注意力允许未来 token 影响过去预测

## 自回归视频-动作建模

Causal World Model 将视频和动作 token 交错在单一自回归序列中：

$$
o_{t+1:t+K} \sim p_\theta(\cdot | o_{\leq t})
$$

然后基于预测的视觉转移用逆动力学模型解码动作：

$$
a_t \sim g_\psi(\cdot | o_t, o_{t+1})
$$

## 关键设计

- **统一潜在空间**：视觉和动作 token 共享潜在空间
- **Mixture-of-Transformers (MoT)**：双 stream 架构，共享注意力
- **Causal Attention Masking**：确保当前预测只依赖过去
- **Closed-loop Rollout**：每步用真实观测重新校准
- **KV-cache / TTT Memory**：缓存历史 key-value 或通过 Test-Time Training 实现常数空间长程记忆

## Causal Latent World Model 变体

在高层语义特征空间（如 DINOv3 特征）而非像素/VAE 空间中进行世界建模，通过解耦交互语义与视觉噪声来提高域泛化能力。

### 与像素世界模型的区别

| | 像素/VAE 世界模型 | Causal Latent World Model |
|---|---|---|
| 生成目标 | 原始像素或 VAE latent | DINOv3 语义特征 |
| 优势 | 视觉真实感强 | 对光照/背景变化鲁棒 |
| 劣势 | 容易过拟合纹理 | 需要预训练视觉特征 |

### 训练目标

统一监督视觉动力学与逆动力学：

$$
\mathcal{L} = \mathcal{L}_{\text{dyn}} + \lambda \mathcal{L}_{\text{inv}}
$$

- 视觉动力学损失：预测下一帧语义/像素特征的速度场
- 逆动力学损失：基于当前与未来观测解码动作

为增强对不完美视觉历史的鲁棒性，训练时对历史特征以概率加噪。

### 内存与延迟优化

- [[04_Embodied-AI/World-Model/Dual-State-TTT-Memory|Dual-State TTT Memory]]：用 Test-Time Training 替代 KV cache，实现 $\mathcal{O}(1)$ 长程记忆
- [[04_Embodied-AI/World-Model/speculative-asynchronous-inference|Speculative Asynchronous Inference (SAI)]]：在机器人执行当前动作块时预去噪下一步，降低约 50% 阻塞延迟

## 与 LingBot-VA

LingBot-VA 是 Causal World Model 的一个实例：

- 基于预训练视频扩散 backbone
- 用 conditional flow matching 自回归生成视频帧
- 动作解码基于预测的视觉转移
- 通过 Noisy History Augmentation 和异步推理降低延迟

## 优缺点

- **优点**：
  - 符合物理因果性
  - 支持实时闭环控制
  - 持久记忆减少长程漂移
  - 视频预测与动作推断相互增强
- **缺点/局限**：
  - 自回归推理延迟高
  - 需要大规模视频预训练
  - 视频生成质量影响控制性能

## Related Concepts

- [[04_Embodied-AI/World-Model/World-Model|World Model]] — Causal World Model 的子类
- [[02_AI/Generative-Models/Flow-Matching|Flow Matching]] — 视频-动作生成的训练目标
- [[02_AI/LLM/Mixture-of-Transformers|Mixture-of-Transformers]] — 共享主干架构
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]] — 与 Causal World Model 是机器人策略的两条路径
- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — CWM 可被视为 WAM 的一种实现
- [[04_Embodied-AI/World-Model/Dual-State-TTT-Memory|Dual-State TTT Memory]] — 长程记忆机制
- [[04_Embodied-AI/World-Model/speculative-asynchronous-inference|Speculative Asynchronous Inference]] — 异步推理降低延迟

## Sources

- [[05_Papers/notes/causal-world-modeling|Causal World Modeling for Robot Control]]
- [[05_Papers/notes/dexworldmodel|DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks]]

### Variable Chunk Size Training

为在部署时灵活选择预测跨度，训练时从预设范围（如 $K \in [1, 8]$）中随机采样 chunk 大小。这样模型学会在不同时间尺度上生成一致预测：

- **大 chunk**：减少自回归步数，单步计算量更大，适合短延迟场景；
- **小 chunk**：更频繁的闭环校正，适合需要高响应精度的任务。

推理时通常取折中值（如 $K=4$）以平衡效率与校正频率。

### Training Objective

统一训练目标同时监督视觉动力学与逆动力学：

$$
\mathcal{L} = \mathcal{L}_{\text{dyn}} + \lambda \mathcal{L}_{\text{inv}}
$$

**视觉动力学损失** 监督未来 latent 帧的速度场：

$$
\mathcal{L}_{\text{dyn}} = \mathbb{E}_{t, s, z_{t+1}, \epsilon} \left[ \| v_\theta(z_{t+1}^{(s)}, s, \tilde{z}_{\leq t}, a_{\leq t} \mid c) - \dot{z}_{t+1}^{(s)} \|^2 \right]
$$

**逆动力学损失** 监督基于当前/未来观测解码动作：

$$
\mathcal{L}_{\text{inv}} = \mathbb{E}_{t, s, a_t, \epsilon} \left[ \| v_\psi(a_t^{(s)}, s, \tilde{z}_{\leq t+1}, a_{\leq t} \mid c) - \dot{a}_t^{(s)} \|^2 \right]
$$

其中 $\tilde{z}$ 为 Noisy History Augmentation 后的视频历史，$c$ 为语言指令。

### 与 Teacher Forcing 的兼容性

Causal World Model 将交错视频-动作序列视为统一序列，用 [[01_Fundamentals/ML/Teacher-Forcing|Teacher Forcing]] 训练。在机器人控制中，Teacher Forcing 的 Exposure Bias 被显著削弱，因为部署时模型会持续接收真实环境观测，与训练时的 ground-truth 上下文机制自然匹配。
