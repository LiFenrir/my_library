---
title: "LiteVLA-H: Dual-Rate Vision-Language-Action Inference for Onboard Aerial Guidance and Semantic Perception"
description: "用于机载空中引导的双速率 VLA 推理系统。"
tags: ["VLA", "Aerial-Robotics", "Edge-Deployment", "Dual-Rate", "Pre-fill-Dominant", "Jetson-Orin", "UAV"]
created: 2026-07-15
---

# LiteVLA-H: Dual-Rate VLA Inference for Onboard Aerial Guidance and Semantic Perception

## 基本信息
- **作者**: Justin Williams, Kishor Datta Gupta, Roy George (Clark Atlanta University), Mrinmoy Sarkar (Siemens Corporation)
- **机构**: Clark Atlanta University, Siemens Corporation
- **链接**: [arXiv:2605.00884](https://arxiv.org/abs/2605.00884)
- **发表**: arXiv preprint, 2026

## 研究背景与动机

VLA 模型在操控任务中表现出色，但**无人机部署**面临更严峻的挑战：必须在严格的计算和通信约束下同时满足**低延迟闭环引导**和**语义场景理解**。

现有空中 VLA 系统（SINGER, VLA-AN, AerialVLA, AIR-VLA）强调导航成功率或基准构建，但忽视了核心调度问题：**同一个边缘 VLA 如何同时支持快速反应引导和慢速语义推理？**

LiteVLA-H 基于 LiteVLA-Edge 提出了**双速率**方案：快速外回路引导 + 慢速语义感知，共享同一个 256M 参数的 backbone。

## 核心方法

### 双速率系统设计

**问题形式化**：设 $I_t$ 为 RGB 观察，$x_t$ 为文本上下文，$m_t \in \{\text{act}, \text{sem}\}$ 为模式变量。

$$y_t = f_\theta(I_t, x_t, m_t)$$

系统需满足两个耦合的时序约束：
$$T_{\text{act}} \leq B_{\text{act}}, \quad T_{\text{sem}} \leq B_{\text{sem}}$$

**调度策略**：$\Delta_s = K\Delta_a,\ K \in \mathbb{N}, K > 1$，实践中使用 K=3（每3个动作周期穿插1次语义刷新），支持事件触发式语义更新。

![[99_Attachments/papers/images/litevla-h/litevla_h_fig1_system.jpg]]

### Pre-fill Dominance 洞察

**核心观察**：紧凑边缘 VLAs 的延迟由 multimodal pre-fill 主导，而非 token 解码：

$$L(n) = P(I_t, x_t, m_t) + \sum_{i=1}^{n} D_i, \quad P \gg D_i \ (\text{for small } n)$$

测量结果：$P \approx 47.8\text{ms}$，边际解码成本 $\approx 1.4\text{ms/token}$。

$$\rho = \frac{47.8}{50.65} \approx 0.944$$

**94.4% 的动作查询延迟在 pre-fill 阶段就已消耗**——意味着仅减少输出 token 数对降低首动作延迟帮助有限。

### 知识保持微调

$$\mathcal{L} = \lambda_a \mathcal{L}_{\text{act}} + \lambda_s \mathcal{L}_{\text{sem}} + \lambda_g \mathcal{L}_{\text{gen}} + \lambda_{kp} \mathcal{L}_{\text{kp}}$$

其中 $\mathcal{L}_{\text{kp}} = \text{KL}(p_{\theta_0}(\cdot|I,x) \| p_\theta(\cdot|I,x))$ 防止灾难性遗忘。

训练数据：120k 反应飞行样本 + 45k 空中语义样本 + 85k 通用 Caption/VQA 样本。

## 实验结果

### 边缘推理延迟

| 任务模式 | 输出复杂度 | 延迟 (ms) | 频率 (Hz) |
|---------|-----------|----------|-----------|
| 反应引导 | 单 action token | 50.65 | 19.74 |
| 场景描述 | 单句 | 149.90 | 6.67 |
| 引导语义 | 2句 + action cue | 153.53 | 6.51 |
| 上下文感知 | 3句 + action cue | 164.57 | 6.08 |

### 延迟分解

| 组件 | 延迟 (ms) |
|------|----------|
| Multimodal pre-fill | 47.8 |
| 边际解码 token | 1.4 |
| 后处理/IPC | 0.3 |
| Vision encoder | 18.2 |
| Projector | 12.5 |
| First-token decoder | 17.1 |

### 消融实验：数据混合

| 变体 | Action Success | CIDEr | Aerial F1 | TTFA (ms) |
|------|---------------|-------|-----------|-----------|
| Action-only | 84.2% | 0.31 | 0.42 | 50.12 |
| Action + Aerial Semantic | 83.5% | 0.45 | 0.81 | 50.35 |
| + Generic Caption/VQA | 82.1% | 0.76 | 0.79 | 50.40 |
| **Full Method** | **83.1%** | **0.82** | **0.80** | 50.65 |

- Action-only 导致严重灾难性遗忘（CIDEr 0.31）
- Full method 在保持 83.1% 成功率的同时，恢复至 0.82 CIDEr

### 调度消融

| 变体 | TTFA (ms) | Action Rate (Hz) | Memory (GB) |
|------|-----------|------------------|-------------|
| 单速率 action-only | 50.65 | 19.74 | 2.1 |
| 单速率 semantic-only | 149.90 | — | 2.2 |
| **Dual-rate (K=3)** | **50.65** | **19.74** | 2.2 |
| ReMem-VLA Style | 98.40 | 10.15 | 3.4 |
| FutureVLA Decoupled | 112.50 | 8.88 | 3.8 |

### 与 SOTA 对比

| Method | Params | Latency (ms) | Rate (Hz) | Success (%) |
|--------|--------|-------------|-----------|-------------|
| OpenVLA-OFT | 7B | 450.0 | 2.2 | 97.1 |
| AnywhereVLA | 450M | 100.0 | 10.0 | 46.0 |
| FutureVLA | 7B | 250.0 | 4.0 | 70.0 |
| ReMem-VLA | 7B | 205.0 | 4.8 | 78.2 |
| LiteVLA-Edge | 256M | 150.5 | 6.6 | 72.5 |
| **LiteVLA-H (action)** | **256M** | **50.65** | **19.74** | **81.3** |
| LiteVLA-H (semantic) | 256M | 149.90 | 6.67 | — |

## 关键创新点

1. **Pre-fill Dominance 发现**：首次明确量化紧凑边缘 VLA 的延迟由 pre-fill 主导（ρ≈0.944），而非 decode，这改变了优化优先级
2. **双速率调度**：19.74 Hz 动作更新 + 6.67 Hz 语义更新，共享同一 backbone，仅增加 0.1 GB 内存和 3.6W 功率
3. **知识保持微调**：动作+语义+通用数据混合训练 + KL 蒸馏正则化，在不牺牲控制性能的前提下保留语义能力
4. **外回路设计选择**：VLA 负责外回路引导，传统飞控负责内回路稳定，分层降低安全风险

## 个人思考与启发

1. **Pre-fill dominance 是关键洞察**：这个发现直接影响了优化方向——应该优先减少视觉 token 数、缓存 prompt 结构、简化 projector，而非优化 decode 速度。这对所有边缘 VLA 设计都有启示。

2. **调度 > 模型架构创新**：本文的核心贡献不是新模型架构，而是调度策略。ReMem-VLA 和 FutureVLA 的记忆/预测模块虽然增强时序推理，但在嵌入式场景下增加了 TTFA。这提醒我们：在资源受限场景中，**调度策略可能比模型能力更关键**。

3. **"快慢结合"的通用范式**：双速率设计（快速反应 + 慢速理解）可能适用于更广泛的机器人场景，不限于无人机。类似 Kahneman 的 System 1 / System 2 思维模型。

4. **局限性**：
   - 闭环飞行评估仅在仿真中进行，真实飞行验证不足
   - 语义保留通过 CIDEr/F1 等代理指标评估，缺乏人类评估
   - K=3 的选择（151.95ms ≈ 149.90ms）具有偶然性，不同硬件配置可能需要重新调参
   - 动作 token 仅适合外回路引导，不能替代经典稳定控制

5. **与 FASTER、VLA-Perf 的关联**：这些同期工作都在强调 time-to-first-action 的重要性，形成了 VLA 系统优化的新共识

## 相关论文

- LiteVLA-Edge: Quantized On-Device Multimodal Control (arXiv:2603.03380)
- LiteVLA: Efficient VLA Control on CPU-bound Edge Robots (arXiv:2511.05642)
- FASTER: Rethinking Real-time Flow VLAs (arXiv:2603.19199)
- VLA-Perf: Demystifying VLA Inference Performance (arXiv:2602.18397)
- LightVLA: Towards Efficient VLAs via Differentiable Token Pruning (arXiv:2509.12594)
- AnywhereVLA: Language-Conditioned Exploration and Mobile Manipulation (arXiv:2509.21006)
- FutureVLA: Joint Visuomotor Prediction for VLA (arXiv:2603.10712)
- ReMem-VLA: Empowering VLA with Memory via Dual-Level Recurrent Queries (arXiv:2603.12942)
- SINGER: Onboard Generalist Vision-Language Navigation Policy for Drones (arXiv:2509.18610)


## 原文

[[05_Papers/articles/litevla-h|litevla-h]]
