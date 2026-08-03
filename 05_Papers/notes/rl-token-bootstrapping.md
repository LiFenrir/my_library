---
title: "RL Token: Bootstrapping Online RL with Vision-Language-Action Models"
description: "用在线 RL token bootstrapping 提升 VLA 模型在机器人操作中的执行精度。"
tags: ["VLA", "Online RL", "Actor-Critic", "Robot Manipulation", "Fine-tuning", "Representation Learning"]
created: 2026-07-15
---

# RL Token: Bootstrapping Online RL with Vision-Language-Action Models

## 基本信息
- **作者**: Charles Xu, Jost Tobias Springenberg, Michael Equi, Ali Amin, Adnan Esmail, Sergey Levine, Liyiming Ke
- **链接**: https://pi.website/research/rlt
- **发表**: Physical Intelligence, 2025

## 研究背景与动机

Vision-Language-Action (VLA) 模型能够从大规模演示数据中学习多样化的操作技能，但在**最后一毫米的执行精度**上往往表现不佳：动作缓慢、需要停顿和重试、小误差在关键阶段会累积成失败。强化学习 (RL) 提供了一种自然的解决方案——通过在目标任务上练习，RL 可以改进对成功最关键的执行阶段。

然而，VLA 的样本高效微调面临两大挑战：
1. **全模型 RL 训练**（如 RECAP、PPO）计算和样本开销大，不适合数小时的快速在线适应；
2. **轻量级 RL 方法**（如 SERL、RL100）虽然样本高效，但使用小型模型（如 ResNet），牺牲了 VLA 的泛化能力。

**核心问题**: 如何在保留 VLA 泛化能力的同时，实现轻量级在线 RL 的速度和样本效率？

## 核心方法

### 方法概述

RLT (RL Token) 的核心思想是：**让预训练的 VLA 暴露一个紧凑的接口（RL token），供轻量级在线 actor-critic 网络使用**。 frozen VLA 提供广泛的感知理解和动作建议，而小型 actor 和 critic 在线适应以改进任务中最困难的部分。

![[99_Attachments/papers/images/rl-token-bootstrapping/d80a12a790bfb47d27e6a3774e399f842b90e4275f6f1edf026343ecf2054dcc.jpg]]

### 1. RL Token 的提取（VLA 适配阶段）

直接对完整 VLA 应用在线 RL 不现实：表示维度高，十亿参数模型的在线更新计算昂贵且样本低效。RLT 通过添加一个**编码器-解码器 transformer** 将 VLA 的内部嵌入压缩为一个紧凑的 RL token。

设 VLA 最后一层 token 嵌入为 $\mathbf{z} = f(s, \ell; \theta_{\mathrm{vla}})$，分解为 $\mathbf{z}_{1:M} = \{\mathbf{z}_1, \ldots, \mathbf{z}_M\}$。

**编码器** $g_\phi$：在序列末尾附加一个可学习的 RL token 嵌入 $\mathbf{e}_{\mathrm{rl}}$，输出该位置的表示即为 RL token：

$$
\mathbf{z}_{\mathrm{rl}} = g_\phi\left(\left[\mathbf{z}_{1:M}, \mathbf{e}_{\mathrm{rl}}\right]\right)_{M+1} \tag{1}
$$

![[99_Attachments/papers/images/rl-token-bootstrapping/648898e52dd511ea0f0f7c6b8705f99cd2b35a05d7e1b36b587d28a2d0318d87.jpg]]

**解码器** $d_\phi$：以自回归方式从 $\mathbf{z}_{\mathrm{rl}}$ 重建原始 VLA 嵌入，使用 stop-gradient 的 VLA 嵌入 $\bar{\mathbf{z}}_i = \mathrm{sg}(\mathbf{z}_i)$：

$$
\mathcal{L}_{\mathrm{ro}} = \mathbb{E}_{\mathcal{D}}\left[\sum_{i=1}^{M} \left\| h_\phi\left(d_\phi\left(\left[\mathbf{z}_{\mathrm{rl}}, \bar{\mathbf{z}}_{1:i-1}\right]\right)\right)_i - \bar{\mathbf{z}}_i \right\|^2 \right] \tag{2}
$$

训练后，VLA 和 RL token 模块均冻结，在线 RL 仅在 $\mathbf{z}_{\mathrm{rl}}$ 上运行。

### 2. 在线 Actor-Critic 微调

**状态表示**: $\mathbf{x} = (\mathbf{z}_{\mathrm{rl}}, \mathbf{s}^\mathrm{p})$，其中 $\mathbf{s}^\mathrm{p}$ 为本体感知状态。

**Critic 训练**: 使用标准 off-policy TD learning，基于 TD3 [19]：

$$
\mathcal{L}_Q = \mathbb{E}_{(\mathbf{x}, \mathbf{a}_{1:C}, \mathbf{x}') \sim \mathcal{B}}\left[\left(\hat{Q} - Q_\psi(\mathbf{x}, \mathbf{a}_{1:C})\right)^2\right]
$$

$$
\hat{Q} = \sum_{t'=1}^{C} \gamma^{t'-1} r_{t'} + \gamma^C \mathbb{E}_{\mathbf{a}' \sim \pi_\theta}\left[Q_{\psi'}(\mathbf{x}', \mathbf{a}')\right] \tag{3}
$$

**Actor 训练**: Actor 不从头生成动作，而是**精炼 (refine)** VLA 提出的参考动作块 $\tilde{\mathbf{a}}_{1:C}$：

$$
\pi_\theta(\mathbf{a}_{1:C} \mid \mathbf{x}, \tilde{\mathbf{a}}_{1:C}) = \mathcal{N}\left(\mu_\theta(\mathbf{x}, \tilde{\mathbf{a}}_{1:C}), \sigma^2 \mathbf{I}\right) \tag{4}
$$

Actor 目标函数包含 critic 值最大化 + 对 VLA 参考动作的 BC 正则化：

$$
\mathcal{L}_\pi(\theta) = \mathbb{E}_{\substack{\mathbf{s} \sim \mathcal{B} \\ \mathbf{a}_{1:C} \sim \pi_\theta}}\left[-Q_\psi(\mathbf{x}, \mathbf{a}_{1:C}) + \beta \|\mathbf{a}_{1:C} - \tilde{\mathbf{a}}_{1:C}\|_2^2\right] \tag{5}
$$

其中参考动作 $\tilde{\mathbf{a}}_{1:C} \sim \pi_{\mathrm{vla}}(\cdot \mid \mathbf{s}, \ell)$。

**Reference Action Dropout**: 随机将部分参考动作替换为零，防止 actor 简单复制 VLA 动作，强制其保持独立动作生成能力。

### 3. 完整系统流程

1. **Warmup**: 用 VLA 参考策略收集数据预填充 replay buffer
2. **Rollout**: VLA 生成参考动作块 + RL token → Actor 输出动作块 → 执行（可选人工干预）
3. **Subsampling**: 以 stride=2 存储中间步骤到 replay buffer，提升数据效率
4. **Update**: 异步执行 off-policy actor-critic 更新，update-to-data ratio = 5
5. **关键阶段针对性改进**: 人工决定何时将控制从 base VLA 切换到 RL policy，集中在最难阶段训练

## 关键创新点

1. **RL Token 表示**: 通过 encoder-decoder 自监督训练，将 VLA 的高维内部嵌入压缩为紧凑的 RL 状态表示，保留任务相关知识的同时实现轻量级在线学习

2. **Action Chunk 上的在线 RL**: 在动作块（$C=10$）而非单步动作上运行 RL，缩短了稀疏奖励下的有效决策时域，解决了高频控制下的信用分配问题

3. **参考动作条件化 + BC 正则化**: Actor 直接以 VLA 采样动作为条件并正则化靠近它，将在线 RL 转化为对强先验的**局部精炼**而非无约束搜索

4. **参考动作 Dropout**: 防止 actor 过度依赖 VLA 参考，保持独立探索能力

5. **关键阶段聚焦**: 仅在任务最关键的高精度阶段应用 RL，其余阶段由 base VLA 处理，大幅提升训练效率

## 实验结果

### 实验任务
在四个需要毫米/亚毫米精度的真实机器人操作任务上评估：
- **螺丝安装** (Screw installation): M3 螺丝拧入螺纹孔，亚毫米对齐
- **扎带紧固** (Zip tie fastening): 双手协调控制可变形物体穿入窄槽
- **以太网插入** (Ethernet insertion): 连接器插入 recessed 端口
- **充电器插入** (Charger insertion): 充电器对齐插入电源插排

![[99_Attachments/papers/images/rl-token-bootstrapping/8278af7d7de79a0cc706bf5ed6935c6d45b02f74ac30b4ceb7dea0654a1c8f33.jpg]]

### 主要结果

**Q1: RLT 是否优于 base VLA？**
- 在所有四个任务的关键阶段，RLT 均提升了成功率和执行速度
- 最难的螺丝安装任务：成功率从 20% 提升至 65%
- 关键阶段速度提升高达 **3x**
- 在以太网任务上，RL policy 甚至**超过了专家遥操作的速度**

![[99_Attachments/papers/images/rl-token-bootstrapping/b74df14074efe65a21110f35a4c407ac25de9f5e7be4464b8903e9680360ab31.jpg]]

![[99_Attachments/papers/images/rl-token-bootstrapping/f03e5ff5d3b652428c716c5d2d115dca8a52c103cb4a649a7374b379a1380358.jpg]]

**Q2: 与替代 RL 方法的比较**
- **HIL-SERL** (单步 RL, ResNet): 在长时域稀疏奖励任务上失败
- **PLD** (单步残差策略): 同样因长时域问题表现不佳
- **DSRL** (latent noise space RL): 成功率高但吞吐量显著低于 RLT
- **DAgger** (模仿学习): 成功率可比较但速度受限于人类演示
- **RLT**: 在保持高成功率的同时，将平均完成步骤减少 **2x**

![[99_Attachments/papers/images/rl-token-bootstrapping/8260b40132ca9f14b7d5a9580b00b5c267fc6ae0b4acefbd01b04ad33b5bc67b.jpg]]

**Q3: 各组件消融实验**
- **w/o RL token** (换为 ResNet-10): 吞吐量下降 50%，证明 RL token 编码了通用视觉编码器不具备的操作相关知识
- **w/o Chunk** (单步动作): 无法可靠达到 base policy 性能，信用分配困难
- **w/o BC Regularizer** ($\beta=0$): 性能下降最大，actor 在仅有 Q-function 梯度下探索整个动作空间
- **w/o Pass-Through** (移除参考动作): 学习变慢，早期探索漂移，训练过程中更多失败

![[99_Attachments/papers/images/rl-token-bootstrapping/1535a770260e6450861803065de9ccd7e9db505c89e631505ea057365a5b7d8d.jpg]]

![[99_Attachments/papers/images/rl-token-bootstrapping/4b8c2035f423cb05e0f7dd9897828dfd871c4b72d80e955d4437e6bd4723e075.jpg]]

**Q4: 涌现策略**
- Base VLA 常表现出"试探"行为：接近目标、后退、重新调整、再尝试
- RLT 学会**流畅插入**：接近端口后直接插入，失败时施加压力并轻微晃动以利用柔顺性
- 这种策略**未在演示数据中出现**，纯粹来自在线探索

![[99_Attachments/papers/images/rl-token-bootstrapping/364c0770b7b1580c28fe57ea998ecfed6fca1f3516eecdab2a2e31e5f23e76e4.jpg]]

### 实现细节
- Base VLA: $\pi_{0.6}$ [33]
- 控制频率: 50 Hz
- 动作块长度: $C = 10$（对应 0.2 秒）
- Actor/Critic: 2-3 层 MLP (hidden dim 256-512)
- 训练数据: 400-1000 episodes，约 15 分钟到 5 小时实际机器人数据
- Update-to-data ratio: 5
- 参考动作 dropout 比例: 50%

## 个人思考与启发

1. **表示压缩的重要性**: RLT 的核心洞察是——与其在 VLA 的高维表示上直接做 RL，不如通过自监督的 encoder-decoder 结构学习一个"瓶颈"表示。这种思路可推广到其他大模型的下游任务适配。

2. **局部精炼 vs 全局搜索**: 将在线 RL 定位为对强先验的局部改进而非无约束搜索，是样本效率的关键。BC 正则化 + 参考动作条件化 + dropout 的组合设计精妙。

3. **Action Chunking 的价值**: 在 50Hz 高频控制下，单步 RL 的信用分配极其困难。Action chunking 将有效时域缩短 10 倍，是方法成功的重要因素。

4. **关键阶段聚焦的实用主义**: 并非所有任务阶段都需要 RL 改进，识别并专注于"瓶颈"阶段是真实世界 RL 部署的实用策略。

5. **局限性**: 方法仍需要人工干预提供奖励信号、干预纠正和阶段切换。完全自主的 RL 改进流水线（如使用奖励模型和进度预测）是未来方向。

## 相关论文

- π0.6* - A VLA That Learns From Experience (RECAP, Physical Intelligence 2025) — 全模型离线 RL 微调 VLA
- HIL-SERL (Luo et al., 2024) — 人在环样本高效 RL，使用 ResNet 编码器
- DSRL (Wagenmaker et al., CoRL 2025) — 在扩散噪声空间中运行 RL
- PLD (Xiao et al., 2025) — 学习单步残差策略
- ConRFT (Chen et al., 2025) — 基于一致性策略的 VLA 强化微调
- Policy Decorator (Yuan et al., ICLR 2025) — 模型无关的在线策略精炼
- GR-RL (Li et al., 2025) — 长时域灵巧操作的 VLA 特化
- π0 (Physical Intelligence, 2024) — 基于流的 VLA 基础模型
- OpenVLA (Kim et al., 2024) — 开源 VLA 模型
- RT-2 (Brohan et al., 2023) — 将网络知识迁移到机器人控制的 VLA
- Diffusion Policy (Chi et al., 2023) — 基于扩散的动作生成
- Cal-QL (Nakamoto et al., NeurIPS 2023) — 校准离线 RL 预训练
- TD3 (Fujimoto et al., 2018) — 双延迟深度确定性策略梯度


## 原文

[[05_Papers/articles/rl-token-bootstrapping|rl-token-bootstrapping]]
