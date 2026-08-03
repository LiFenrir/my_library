---
title: "DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks"
description: "面向机器人灵巧操作的因果潜在世界模型，支持自动化任务学习与 Sim2Real 迁移。"
tags: ["具身智能", "World Model", "Causal Learning", "Robotics", "VLA", "Diffusion", "Sim2Real", "TTT", "DINOv3"]
created: 2026-07-15
---

# DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks

## 基本信息
- **作者**: DexForce AI Team of Physical AI
- **链接**: [arXiv](https://arxiv.org/abs/...)（待补充）
- **发表**: arXiv preprint, 2026

## 研究背景与动机

当前将生成式 World-Action Model（WAM）部署到机器人操作任务中面临三大瓶颈：

1. **冗余像素级重建（Pixel-level Reconstruction）**：传统 WAM 直接在像素空间或 VAE latent space 中建模未来状态，迫使模型浪费大量容量重建与任务无关的视觉细节（如光照变化、杂乱背景），限制了交互语义特征的提取和域泛化能力。
2. **内存随序列线性增长**：标准因果世界模型的 KV Cache 随自回归生成步数线性增长 $\mathcal{O}(T)$，在长程操作任务中导致严重的内存耗尽和推理延迟。
3. **顺序推理延迟**：传统 VLA 策略是反应式的，必须等待物理执行完成、获取下一帧观测后才能启动下一次推理，造成严重的顺序延迟瓶颈。

此外，机器人数据收集成本高昂，传统静态数据集难以支撑模型规模的快速增长。

## 核心方法

### 1. Causal Latent World Model (CLWM)

CLWM 采用 **DINOv3 特征作为生成目标**，替代低层像素重建：

$$
f_t = \Phi_{\mathrm{DINO}}(o_t) \in \mathbb{R}^{C \times H' \times W'}
$$

其中 $H' = H/P$, $W' = W/P$, $P=16$ 为 DINOv3 base 模型的 patch size。由于 DINOv3 空间对视觉噪声和背景变化天然鲁棒，在语义空间中生成序列有效绕过了像素重建的计算负担，将模型容量严格用于交互语义的时间演化。

CLWM 采用 **Mixture of Transformers (MoT)** 架构：
- **Latent Video Model** $\phi_{\mathrm{vid}}$：预测未来 latent video 特征
- **Action Model** $\phi_{\mathrm{act}}$：解码对应的动作块
- 两者共享核心 Transformer blocks（从 Wan2.2-5B 初始化），仅使用 domain-specific 的 flow timestep embedding 和线性输入/输出投影层：

$$
\phi_{\mathrm{vid}} = \phi_{\mathrm{vid}}^{\mathrm{out}} \circ \phi_{\mathrm{share}} \circ \phi_{\mathrm{vid}}^{\mathrm{in}}; \quad \phi_{\mathrm{act}} = \phi_{\mathrm{act}}^{\mathrm{out}} \circ \phi_{\mathrm{share}} \circ \phi_{\mathrm{act}}^{\mathrm{in}}
$$

**两阶段自回归 Flow Matching**：

**Stage 1: Latent Video Flow Matching**

$$
\mathcal{L}_{\mathrm{video}} = \mathbb{E}_{s, \epsilon_{\mathrm{vid}}, f_{t+1}, h_t, l} \left[ \left\| v_{\phi_{\mathrm{vid}}}\left(f_{t+1}^{(s)}, s \mid h_{\leq t}, l\right) - \dot{f}_{t+1}^{(s)} \right\|^2 \right]
$$

其中 $f_{t+1}^{(s)} = (1-s)\epsilon_{\mathrm{vid}} + s \cdot f_{t+1}$，$\dot{f}_{t+1}^{(s)} = f_{t+1} - \epsilon_{\mathrm{vid}}$。

**Stage 2: Action Flow Matching**

为增强 Action Model 对不完美视觉历史的鲁棒性，训练时以概率 $p=0.5$ 向历史 latent 特征注入高斯噪声：

$$
\tilde{f}_{\leq t} = \begin{cases} (1-s_{\mathrm{aug}})\epsilon + s_{\mathrm{aug}} \cdot f_{\leq t}, & p=0.5, s_{\mathrm{aug}} \in [0.5, 1], \epsilon \sim \mathcal{N}(0, I) \\ f_{\leq t}, & 1-p=0.5 \end{cases}
$$

Action Model 的优化目标：

$$
\mathcal{L}_{\mathrm{action}} = \mathbb{E}_{s, \epsilon_{\mathrm{act}}, a_t, \tilde{h}_t, l, \tilde{f}_{t+1}} \left[ \left\| v_{\phi_{\mathrm{act}}}\left(a_t^{(s)}, s \mid \tilde{h}_{\leq t}, l, \tilde{f}_{t+1}\right) - \dot{a}_t^{(s)} \right\|^2 \right]
$$

![[99_Attachments/papers/images/dexworldmodel/a6df7136671f5df268e0600fc800404a42ea531742dd12d5d5474612e8010687.jpg]]
*Figure 1. CLWM 整体架构。采用 MoT 统一 latent video model 和 action model，通过共享 TTT Memory 维护历史上下文。*

### 2. Dual-State Test-Time Training (TTT) Memory

传统 Transformer 的 KV Cache 随序列长度线性增长 $\mathcal{O}(T)$。CLWM 用 **TTT-MLP** 替代 KV Cache，将历史上下文内化到动态可更新的神经网络权重中，实现严格的 **$\mathcal{O}(1)$ 内存占用**。

**TTT Layer 定义**：

对于输入 token $z_t \in \mathbb{R}^{L \times D}$，自监督重建任务参数化为：

$$
\ell_{\mathrm{self}}(\mathcal{W}; z_t) = \left\| f(\theta_K z_t; \mathcal{W}) - \theta_V z_t \right\|^2
$$

其中 $f_{TTT_{mlp}}(x; \mathcal{W}) = x + \mathrm{LN}(\mathrm{MLP}(x; \mathcal{W}))$，使用 GELU 激活和 $4\times$ 扩展因子。

更新后的权重通过 query 投影提取 hidden state：

$$
l_t = f_{TTT_{mlp}}(\theta_Q z_t; \mathcal{W}_t)
$$

并通过门控机制稳定微调：

$$
f_{TTT}(z_t; \mathcal{W}_t) = \tanh(\alpha) \otimes f_{TTT_{mlp}}(\theta_Q z_t; \mathcal{W}_t) + z_t
$$

**Dual-State 更新策略**：

![[99_Attachments/papers/images/dexworldmodel/f4b79147baf3b7626eb7f3adaa4d9d8f33e1aa1eecb942d61e1d321d42619ba3.jpg]]
*Figure 2(a). 标准因果注意力依赖 KV Cache。*

![[99_Attachments/papers/images/dexworldmodel/3436f58d3e966b0e85a1654954292ddfd4b9e077d3bff1a7eb5b39cdd41f683b.jpg]]
*Figure 2(b). TTT Memory 替代 KV Cache。*

![[99_Attachments/papers/images/dexworldmodel/75f377a5d1b785a16f73505c87c2cbb0ec2c010cf2393cc68127a5ebe42389ae.jpg]]
*Figure 2(c). Dual-State TTT Memory 更新策略。*

1. **Long-Term TTT Memory（锚点）**：仅当接收到真实物理观测时更新，维护真实环境因果性：

$$
\mathcal{W}_t^{\mathrm{long}} = \mathcal{W}_{t-1}^{\mathrm{long}} - \eta \nabla_{\mathcal{W}} \ell_{\mathrm{self}}(\mathcal{W}_{t-1}^{\mathrm{long}}; h_t)
$$

2. **Working TTT Memory（分支）**：生成阶段从 Long-Term Memory fork 而来，在 ODE 积分期间保持冻结。

3. **$s=0$ 中间更新**：Latent Video 预测完成后，Working Memory 吸收预测的未来状态进行瞬时更新，为后续 Action 解码提供上下文：

$$
\mathcal{W}_t^{\mathrm{work}'} \leftarrow \mathcal{W}_t^{\mathrm{work}} - \eta \nabla_{\mathcal{W}} \ell_{\mathrm{self}}(\mathcal{W}_t^{\mathrm{work}}; \hat{f}_{t+1})
$$

### 3. Speculative Asynchronous Inference (SAI)

利用世界模型的前向预测能力，将扩散去噪与物理执行深度重叠：

![[99_Attachments/papers/images/dexworldmodel/1d6352288c5ea0f265593148bd09078c68a328100488e862825b47b7ad7e1798.jpg]]
*Figure 3(a). 传统自回归世界模型推理流水线。*

![[99_Attachments/papers/images/dexworldmodel/7cec879d7d9564cf4282a12a9b3ba14c52c758fefbf39670f7bbc44d3cd64d34.jpg]]
*Figure 3(b). Speculative Asynchronous Inference 流水线。*

- **Phase 1: Speculative Pre-Denoising**：在机器人执行当前动作块 $a_{t-1}$ 时，利用上一时刻预测的未来语义特征 $\hat{f}_t$ 作为代理观测，主动启动下一时刻的 flow matching，从 $s=0$ 积分到中间阈值 $s=s_{\mathrm{mid}}$。
- **Phase 2: Instantaneous Calibration**：物理执行完成后，用真实观测 $f_t$ 校准 Long-Term Memory，ODE 从 $s_{\mathrm{mid}}$ 继续积分到 $s=1$，仅需计算剩余的细粒度去噪步骤。

SAI 将每块推理延迟降低约 **50%**。

### 4. EmbodiChain：在线数据流训练框架

EmbodiChain 通过 **Efficiency Law**（具身智能的效率定律）实现规模化训练：

> 具身训练的有效性主要取决于学习过程中维持新鲜、多样、物理有效的经验流的连续性。

![[99_Attachments/papers/images/dexworldmodel/9e139cd5bbdaa75b05e7a2c006a9f3db8a126ecced3d30d86dd59a725cc229ff.jpg]]
*Figure 4. Efficiency Law：损失作为数据生成速率的函数。*

**核心组件**：

1. **Generative Simulation**：
   - **Asset Generation**：用生成模型生成 3D mesh，通过多目标优化几何、尺度和坐标系，导出含物理/语义元数据的 USD 文件。
   - **Scene Layout Synthesis**：生成初始布局，前景交互物体放置在机器人运动学可行区域内，背景资产通过梯度优化消除碰撞。

![[99_Attachments/papers/images/dexworldmodel/630254ceb36f38a565d491b9f4c53e62ea63282128916ddf305001b3fa8218e4.jpg]]
*Figure 5. 铰接式 3D 物体生成流程。*

![[99_Attachments/papers/images/dexworldmodel/4a45ca812010e7f08622d1106d2281994afc6e033d24f4aff0f1c1bcaaf00fe7.jpg]]
*Figure 6. 生成的机器人学习环境场景布局示例。*

2. **Domain Expansion**：
   - **Reachability-Aware Sampling**：在任务相关运动空间中采样候选机器人状态，最大化末端执行器接近方向、接触几何和交互结果的差异性。
   - **Closed-loop Error Recovery**：失败时生成纠正运动轨迹，重新标注并整合到数据集中。
   - **Visual Augmentation**：动态采样光照温度、BRDF 属性、传感器漂移等环境因子，通过平滑随机过程保持时间一致性。
   - **Physics-Grounded Generation**：确保所有扩展域严格遵守经典力学原理。

![[99_Attachments/papers/images/dexworldmodel/ee06e0cd87f4cf0516e1480daa8863e73fa71f1353895fc0043fc66f8dd0ac99.jpg]]
*Figure 7. 机器人工作空间可视化。*

3. **Online Data Streaming (ODS)**：
   - 无存储范式，持续合成并直接注入新鲜轨迹到优化器。
   - 异构共享内存流水线：仿真和生成 worker 异步写入 lock-free 循环缓冲区，learner worker 通过 zero-copy 消费 batch。
   - 统一了 Online RL 的反应性和 Offline RL 的计算稳定性。

## 关键创新点

1. **DINOv3 作为生成目标**：首次将 DINOv3 latent features 用作世界模型的生成目标，从根本上解耦交互语义与冗余视觉纹理，实现卓越的域泛化。
2. **$\mathcal{O}(1)$ 常数内存 TTT Memory**：用 Dual-State TTT-MLP 替代 KV Cache，严格保证常数内存占用，解锁无约束的长程推理。
3. **Speculative Asynchronous Inference**：利用前向预测能力将扩散预去噪隐藏在物理执行背后，降低约 50% 阻塞延迟。
4. **EmbodiChain & Efficiency Law**：建立具身智能效率定律，通过在线数据流持续注入物理有效的多样化经验，实现前所未有的 zero-shot sim-to-real 迁移。

## 实验结果

### 仿真结果（RoboTwin）

在 RoboTwin 双臂操作基准上，CLWM 在 48 项任务中达到 **94.00%** 平均成功率，显著优于基线：

| 方法 | 平均成功率 |
|------|-----------|
| $\pi_{0.5}$ | 76.76% |
| X-VLA | 72.84% |
| Motus | 87.02% |
| LingBot-VA | 91.55% |
| **CLWM (Ours)** | **94.00%** |

### 效率分析

- **常数内存**：在 2000 步长程操作 episode 中，TTT Memory 保持严格平坦的 $\mathcal{O}(1)$ 内存占用，而 KV Cache 线性增长。
- **延迟降低**：SAI 将端到端阻塞延迟降低约 **50%**。

### EmbodiChain 消融实验

**Domain Expansion 消融**（ID / OOD）：

| 配置 | ID 成功率 | OOD 成功率 |
|------|----------|-----------|
| Baseline (Spatial Randomization) | 64% | 25% |
| + Visual Augmentation | 75% | 42% |
| + Physics-grounded Generation | 81% | 56% |
| + Reachability-aware Sampling (Full) | **95%** | **82%** |

**Online Data Streaming 消融**：

| 训练配置 | Hanging Mug | Turn Switch | Stack Bowls |
|---------|------------|------------|------------|
| Static Baseline | 62% | 85% | 88% |
| ODS$_{\text{sample 213}}$ | 60% | 84% | 85% |
| ODS$_{\text{sample 50}}$ | 92% | 92% | 96% |
| ODS$_{\text{sample 10}}$ | **96%** | **98%** | **98%** |

ODS 中 replay bound 越低（数据周转越快），性能越好，验证了 Efficiency Law。

### 真机部署（Zero-Shot Sim-to-Real）

在 Agilex CobotMagic 双臂平台上测试 4 项日常操作任务，CLWM **仅用仿真数据训练**，实现 zero-shot 迁移：

| 方法 | 双臂倒水 | 桌面整理 | 物品交接与放置 | 开盖与放置 |
|------|---------|---------|--------------|-----------|
| $\pi_0$ (50 real demos) | 25% | 20% | 20% | 5% |
| GR00T N1.5 (50 real demos) | 35% | 20% | 15% | 5% |
| Sim2Real-VLA | 80% | 80% | 40% | 35% |
| **CLWM (Ours)** | **95%** | **90%** | **80%** | **65%** |

CLWM 在 zero-shot 设定下显著优于使用 50 条真实人类演示微调的基线。

## 个人思考与启发

1. **语义空间生成 vs 像素空间生成**：CLWM 用 DINOv3 特征替代像素作为生成目标是一个极具洞察力的设计。它借鉴了视觉表征学习中"语义解耦"的思想，将世界模型的职责从"重建世界"收窄为"预测交互语义演化"，这与人类认知中"关注任务相关特征而忽略背景噪声"的方式更为接近。对于其他具身智能任务，类似的预训练视觉特征（如 MAE、CLIP）是否也能起到类似作用值得探索。

2. **TTT Memory 的范式转移**：从"存储历史 token"到"将历史内化到模型权重"是一种根本性的架构创新。$\mathcal{O}(1)$ 内存不仅解决了长程任务的工程瓶颈，更暗示了智能体记忆的本质可能不是数据库式的检索，而是参数化的压缩。Dual-State 的设计（锚点 + 工作记忆）也巧妙地平衡了真实因果与预测推理的需求。

3. **SAI 的物理-计算协同**：SAI 的核心洞察是"世界模型已经预测了未来，为什么不利用这个预测来提前计算？"这种将算法复杂度与部署延迟解耦的思路，对于任何需要高频闭环控制的系统都有借鉴意义。

4. **Efficiency Law 的启示**：论文明确提出"具身智能的瓶颈不是模型大小，而是经验生成效率"。ODS 将数据生成与训练无缝耦合，本质上是在做"在线课程学习"——模型永远面对新鲜样本，无法过拟合。这与传统大模型"预训练 + 微调"的范式形成鲜明对比，可能是具身智能特有的 scaling law。

5. **局限与展望**：
   - 论文未详细讨论 TTT 的学习率 $\eta$ 对稳定性的影响，以及不同任务长度下的鲁棒性。
   - DINOv3 特征空间是否足够表达细粒度操作（如力控、滑动接触）仍需验证。
   - EmbodiChain 的仿真生成虽然多样，但真实世界中的不可预测因素（如人类干扰、非刚性物体）仍是挑战。

## 相关论文

- π0: A vision-language-action flow model for general robot control
- LingBot-VA: Causal world modeling for robot control
- Motus: A unified latent action world model
- DINOv3: Learning robust visual features without supervision
- TTT: Learning to (learn at test time): RNNs with expressive hidden states
- Wan2.1: Open and advanced large-scale video generative models
- RoboTwin: A scalable data generator and benchmark for bimanual manipulation
- EmbodiChain: An end-to-end GPU-accelerated platform for embodied intelligence


## 原文

[[05_Papers/articles/dexworldmodel|dexworldmodel]]
