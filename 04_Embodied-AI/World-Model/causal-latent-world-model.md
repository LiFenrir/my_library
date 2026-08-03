---
title: "Causal Latent World Model"
description: "在 DINOv3 等语义特征空间中进行因果生成建模的世界模型"
tags: [concept, embodied-ai, world-model]
created: 2026-07-29
---

# Causal Latent World Model (CLWM)

**核心定义**：Causal Latent World Model 是在高层语义特征空间（如 DINOv3 特征）而非像素/VAE 空间中进行世界建模的方法，通过解耦交互语义与视觉噪声来提高域泛化能力。

## 核心设计

- **DINOv3 特征作为生成目标**：避免重建冗余像素细节
- **Dual-State TTT Memory**：通过 Test-Time Training 实现长程记忆的常数空间复杂度
- **Speculative Asynchronous Inference (SAI)**：将部分扩散去噪隐藏在物理执行背后，降低阻塞延迟约 50%

## 与像素世界模型的区别

| | 像素/VAE 世界模型 | Causal Latent World Model |
|---|---|---|
| 生成目标 | 原始像素或 VAE latent | DINOv3 语义特征 |
| 优势 | 视觉真实感强 | 对光照/背景变化鲁棒 |
| 劣势 | 容易过拟合纹理 | 需要预训练视觉特征 |

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/World-Model|World Model]] — CLWM 是世界模型的一种
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 同属因果世界模型家族
- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — CLWM 可被视为 WAM 的一种实现

## 方法细节

### DINOv3 语义特征作为生成目标

CLWM 使用冻结的 DINOv3 base 模型作为特征提取器：

$$
f_t = \Phi_{\mathrm{DINO}}(o_t) \in \mathbb{R}^{C \times H' \times W'}
$$

其中 $H' = H / P$, $W' = W / P$，默认 patch size $P = 16$。

相比像素或 VAE 纹理 latent，DINOv3 特征对光照、背景变化更鲁棒，使模型专注于交互语义的时间演化。

### Mixture-of-Transformers (MoT) 共享主干

Latent Video Model $\phi_{\mathrm{vid}}$ 与 Action Model $\phi_{\mathrm{act}}$ 共享核心 Transformer 块，仅在输入/输出投影层和流时间嵌入上保持域相关：

$$
\phi_{\mathrm{vid}} = \phi_{\mathrm{vid}}^{\mathrm{out}} \circ \phi_{\mathrm{share}} \circ \phi_{\mathrm{vid}}^{\mathrm{in}}; \quad \phi_{\mathrm{act}} = \phi_{\mathrm{act}}^{\mathrm{out}} \circ \phi_{\mathrm{share}} \circ \phi_{\mathrm{act}}^{\mathrm{in}}
$$

这种参数共享强制视觉动力学与逆动力学在统一表示空间中对齐。

### Stage 1：Latent Video Flow Matching

给定历史记忆 $h_{\leq t}$ 和语言 $l$，Latent Video Model 将噪声 $\epsilon_{\mathrm{vid}}$ 去噪为下一帧语义特征 $f_{t+1}$：

$$
\mathcal{L}_{\mathrm{video}} = \mathbb{E}_{s, \epsilon_{\mathrm{vid}}, f_{t+1}, h_t, l} \left[ \left\| v_{\phi_{\mathrm{vid}}}(f_{t+1}^{(s)}, s \mid h_{\leq t}, l) - \dot{f}_{t+1}^{(s)} \right\|^2 \right]
$$

其中 $f_{t+1}^{(s)} = (1-s)\epsilon_{\mathrm{vid}} + s f_{t+1}$，$\dot{f}_{t+1}^{(s)} = f_{t+1} - \epsilon_{\mathrm{vid}}$。

### Stage 2：Action Flow Matching

Action Model 基于历史、语言与 Stage 1 预测的未来语义 $\hat{f}_{t+1}$ 解码动作块 $a_t = \{a_{t,1}, \dots, a_{t,\tau}\}$，其中 $\tau$ 为动作块大小（视觉帧与动作 token 的时间比例，论文中 $\tau = 16$）。

为增强对不完美视觉历史的鲁棒性，训练时以概率 $p=0.5$ 对历史特征加噪：

$$
\tilde{f}_{\leq t} = \begin{cases}
(1 - s_{\mathrm{aug}})\epsilon + s_{\mathrm{aug}} f_{\leq t}, & p = 0.5, \quad s_{\mathrm{aug}} \in [0.5, 1], \quad \epsilon \sim \mathcal{N}(0, I) \\
f_{\leq t}, & 1 - p = 0.5
\end{cases}
$$

动作流匹配目标：

$$
\mathcal{L}_{\mathrm{action}} = \mathbb{E}_{s, \epsilon_{\mathrm{act}}, a_t, \tilde{h}_{\leq t}, l, \tilde{f}_{t+1}} \left[ \left\| v_{\phi_{\mathrm{act}}}(a_t^{(s)}, s \mid \tilde{h}_{\leq t}, l, \tilde{f}_{t+1}) - \dot{a}_t^{(s)} \right\|^2 \right]
$$

### 内存与延迟优化

- [[04_Embodied-AI/World-Model/Dual-State-TTT-Memory|Dual-State TTT Memory]] 用 Test-Time Training 替代 KV cache，实现 $\mathcal{O}(1)$ 长程记忆。
- [[04_Embodied-AI/World-Model/speculative-asynchronous-inference|Speculative Asynchronous Inference (SAI)]] 在机器人执行当前动作块时预去噪下一步，降低约 50% 阻塞延迟。

## 与相关概念的关系

- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — CLWM 同属因果世界模型家族，强调时间因果性
- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — CLWM 是 WAM 在语义特征空间的实现
- [[04_Embodied-AI/World-Model/test-time-training-for-world-models|Test-Time Training for World Models]] — CLWM 中的记忆机制
- [[04_Embodied-AI/World-Model/speculative-asynchronous-inference|Speculative Asynchronous Inference]] — CLWM 中的推理调度机制
- [[04_Embodied-AI/World-Model/embodichain|EmbodiChain]] — CLWM 配套的生成式数据管线
- [[02_AI/Flow-Matching|Flow Matching / CFM]] — CLWM 的生成目标
- [[04_Embodied-AI/World-Model/Noisy-History-Augmentation|Noisy History Augmentation]] — 训练动作模型适应带噪历史

## 来源

- [[05_Papers/articles/dexworldmodel|DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks]]
