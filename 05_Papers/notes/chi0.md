---
title: "χ0: Resource-Aware Robust Manipulation via Taming Distributional Inconsistencies"
description: "通过驯服数据、策略与部署三分布不一致性实现资源感知的鲁棒操作。"
tags: ["具身智能", "Resource-Aware", "Robust Manipulation", "Distributional Inconsistencies"]
created: 2026-07-15
---

# χ0: Resource-Aware Robust Manipulation via Taming Distributional Inconsistencies

## 基本信息
- **作者**: Checheng Yu, Chonghao Sima, Gangcheng Jiang, Hai Zhang, Haoguang Mai, Hongyang Li, Huijie Wang, Jin Chen, Kaiyang Wu, Li Chen, Lirui Zhao, Modi Shi, Ping Luo, Qingwen Bu, Shijia Peng, Tianyu Li, Yibo Yuan (Kinetix AI)
- **链接**: [Code](https://github.com/OpenDriveLab/kai0) | [Blog](https://mmlab.hk/research/kai0)
- **发表**: arXiv, 2025

## 研究背景与动机

机器人操作中的核心瓶颈并非单纯的资源规模（数据量、算力），而是**三个关键分布之间的不一致性（distributional inconsistencies）**：

- $P_{\text{train}}$：人类专家示教数据的分布
- $Q_{\text{model}}$：策略学习到的归纳偏置分布
- $P_{\text{test}}$：真实部署时执行轨迹的分布

这种分布不一致性在长程（long-horizon）、接触丰富（contact-rich）的可变形物体操作任务中尤为突出，导致错误累积（compounding errors）和系统鲁棒性不足。传统方法通过大规模数据收集和算力扩展来缓解，但成本极高且未触及根本问题。

本文以**协作式双臂服装操作**（flattening, folding, hanging）为测试场景，提出了 χ0（KAI 0）框架，以资源高效的方式系统性地解决上述分布不匹配问题。

> 命名由来：Kinetics Aligned to Intelligence（KAI），取希腊字母 χ 与 KAI 谐音，致敬 π 系列策略。

![[99_Attachments/papers/images/chi0/c01ce57f349ad7764779d31865995ed6451fca25516f4fd1c53cbc9f01f7d91b.jpg]]

## 核心方法

χ0 围绕三大技术支柱构建，分别对应三种分布不一致性的对齐：

### 1. Model Arithmetic (MA) — 对齐 $Q_{\text{model}}$ 与 $P_{\text{train}}$

**问题**：有限的专家示教导致 $P_{\text{train}}$ 对高维解流形覆盖不足，策略 $Q_{\text{model}}$ 产生偏置。

**方法**：在权重空间（weight space）中合并（merge）多个在互补数据子集上独立训练的策略检查点（checkpoints）：

$$
\theta_{\text{merged}} = \sum_{i=1}^{n} \alpha_i \theta_i, \quad \text{s.t. } \alpha_i \geq 0, \; \sum_{i=1}^{n} \alpha_i = 1
$$

其中 $\{\alpha_i\}$ 通过在**OOD 验证集**（DAgger 收集的恢复轨迹）上的损失最小化来确定。

**关键设计**：
- 使用 DAgger 数据作为 OOD 验证集，确保合并后的策略泛化到未见过的失败恢复状态
- 对比了四种合并策略：Average Weighting、Inverse Loss、Gradient Descent、Greedy Search，其中 **Greedy Search** 表现最优
- 无需额外数据收集，也无需 MoE 的路由机制或模型集成的推理开销

![[99_Attachments/papers/images/chi0/d00424b791775c823dd5285a1fdb9d968605865b76140d1a6f1b81680ce7363e.jpg]]

### 2. Stage Advantage (SA) — 优化 $Q_{\text{model}}$ 以适应 $P_{\text{test}}$

**问题**：长程任务中，视觉相似但语义不同的状态会导致策略误用行为；传统的 value-difference 优势估计 $A(s,a) = V(s') - V(s)$ 会放大帧级估计噪声，且多阶段任务中 $V(s)$ 存在多值歧义。

**方法**：
- 将优势估计重新建模为**直接预测**：$A(s,a) = f_\theta(s, s')$，避免误差累积
- 引入**阶段感知（stage-aware）**标签：将长程任务分解为语义子目标（stages），优势估计以当前阶段为条件：

$$
A_{\text{stage}}(s, a, g) = f_\theta(s, s' \mid g)
$$

其中 $g \in \{0, \frac{1}{S}, \dots, \frac{S-1}{S}\}$ 为阶段标签，$S$ 为阶段数。

- 将连续优势预测二值化为最优性指示器：$I = \mathbb{1}[A_{\text{stage}} > \epsilon]$，用于 advantage-weighted behavior cloning

**优势**：相比 $\pi_{0.6}^*$ 的 value-difference 方法，SA 具有更好的数值稳定性（numerical stability），表现为更低的训练损失和更平滑的帧间预测。

![[99_Attachments/papers/images/chi0/7e1054833671a29f773a541e3bcb919adc3426e97045e7e8f96ac1184f3e4269.jpg]]

### 3. Train-Deploy Alignment (TDA) — 桥接 $P_{\text{train}}$ 与 $P_{\text{test}}$

**问题**：推理-执行延迟导致动作错位；静态示教缺乏恢复行为；$P_{\text{train}}$ 与 $P_{\text{test}}$ 之间存在分布漂移。

**方法包含三个互补策略**：

**(a) Temporal Chunk-wise Smoothing（时序块级平滑）**

解决 action chunking 策略中连续推理块之间的时序不连续问题。维护当前动作缓冲区 $\mathbf{a}^{\text{old}}$ 和新预测块 $\mathbf{a}^{\text{new}}$，通过重叠区域的线性插值实现平滑过渡：

$$
w_i = 1 - \frac{i}{\max(L-1, 1)}, \quad \tilde{a}_i = w_i a_i^{\text{old}} + (1 - w_i) a_{\text{rem},i}^{\text{new}}
$$

其中 $L$ 为重叠长度，$d_{\max}$ 为丢弃阈值以处理推理延迟。

**(b) Heuristic DAgger**

传统 DAgger 需要等待策略自然失败后再人工干预，耗时且低效。Heuristic DAgger 直接**从人工设计的失败状态初始化**（如错位抓取、部分掉落），收集恢复示教，将失败经验前置到数据收集中。

**(c) Spatio-temporal Augmentation**

- 水平翻转 + 左右臂交换
- 部分帧跳过（frame-skipping）以合成速度变化

![[99_Attachments/papers/images/chi0/13223354403485a83a3220c5b908368ec038de28ea215d030b823d9688fb3a40.jpg]]

## 关键创新点

1. **系统性分布对齐框架**：首次将机器人学习的全周期（数据收集-模型训练-策略部署）形式化为三个分布 $P_{\text{train}}, Q_{\text{model}}, P_{\text{test}}$ 的对齐问题，并针对每种不一致性提出针对性模块

2. **Model Arithmetic**：利用权重空间合并实现资源高效的策略覆盖扩展，OOD 验证（DAgger 数据）指导合并权重，优于全数据联合训练

3. **Stage Advantage**：将优势估计从 value-difference 转为直接预测，并引入阶段条件解决多值歧义，显著提升数值稳定性

4. **Temporal Chunk-wise Smoothing**：轻量级的时序平滑算法，无需修改模型架构，有效缓解推理-执行延迟导致的控制不稳定性

5. **Heuristic DAgger**：通过预设失败状态加速恢复行为数据收集，降低 DAgger 的时间成本

## 实验结果

### 实验设置
- **硬件**：两套双臂机器人系统（Agilex Piper + ARX X5），各配 3 个 Intel RealSense D435i 相机
- **数据**：每任务约 20 小时专家示教，共 2668 (Task A) / 3519 (Task B) / 2988 (Task C) 条轨迹
- **训练**：基于 $\pi_{0.5}$ 全参数微调，Flow Matching 目标，$8 \times \text{A100}$ GPU，80k steps
- **基线**：$\pi_{0.5}$（主要基线）、$\pi_0$

### 评估任务
| 任务 | 难度 | 描述 |
|------|------|------|
| Task A | Easy | T-shirt 展平与折叠 |
| Task B | Medium | 条件检索与分类（T-shirt 折叠/衬衫移交）|
| Task C | Hard | 衬衫悬挂 |

### 核心结果
- **χ0 相比 $\pi_{0.5}$ 成功率提升约 250%**
- 仅使用 20 小时数据和 8 张 A100 实现高可靠自主运行，完成 **24 小时连续无间断** 压力测试

### 模块消融

**系统功效分解（Task A）**：
- SA 是 throughput 的主导因素
- TDA 驱动成功率但增加 retry cost
- 各模块叠加后性能单调提升

![[99_Attachments/papers/images/chi0/d9a71be36f38dc844a72953758cf055d82565a300e878084cf37d02d5fc9e581.jpg]]

**Model Arithmetic**：
- 所有 MA 变体均优于 single-best 和 full-data 基线
- OOD 验证比 in-domain 验证更稳定（标准误更低）
- Greedy Search 策略最优

![[99_Attachments/papers/images/chi0/c9f8d8cb39e3f1cd5c1a19626107c1c45737abe167f030d224a72212c77f525c.jpg]]

**Stage Advantage**：
- SA 在 Smooth Frame Ratio (SFR) 和 Mean Squared Temporal Difference (MSTD) 上均优于 $\pi_{0.6}^*$ 风格基线
- 数值稳定性提升与最终性能提升正相关

![[99_Attachments/papers/images/chi0/10ab16d210436a45e72a6e2323cc1d94c8dd9bdbe9bb218df3a6f5a4c38b7eff.jpg]]

**Train-Deploy-Alignment**：
- Heuristic DAgger 显著提升失败恢复能力和整体性能
- Temporal chunk-wise smoothing 优于 temporal ensembling 和 RTC，与 RTC 结合可进一步提升

![[99_Attachments/papers/images/chi0/e038725fedb3aa9237d71d6e4d04baf95de65df87e013f1ba930b6e60cc17647.jpg]]

## 个人思考与启发

1. **分布视角的价值**：将机器人学习的挑战重新框定为分布对齐问题，比单纯追求数据/算力规模更具指导意义。这种框架化思考有助于识别真正的瓶颈所在。

2. **Model Arithmetic 的启示**：权重合并不仅是一种模型融合技巧，更是一种"资源高效地扩展策略覆盖"的范式。OOD 验证集的设计（DAgger 恢复轨迹）是关键，说明**验证集的选择应反映部署时的真实分布**。

3. **Stage Advantage 的设计哲学**：从间接估计（value difference）转向直接预测（pairwise prediction），并引入语义阶段条件，体现了"降低方差、消除歧义"的统计直觉。这对其他长程决策任务也有借鉴意义。

4. **Heuristic DAgger 的实用性**：传统 DAgger 的瓶颈在于等待自然失败。通过主动构造失败状态，可以大幅降低数据收集成本，这对实际机器人部署非常有价值。

5. **数据质量的核心地位**：作者在附录中强调数据质量是策略性能波动的首要因素（20%-60% 的成功率差异），并提出 **replay-ability** 作为数据有效性的核心原则。这提醒我们在追求算法创新的同时，不能忽视数据工程的基础作用。

6. **局限性**：
   - 未显式评估预训练先验在 post-training 中的保留程度
   - 数据质量评估仍依赖昂贵的完整训练循环或回放检查
   - 目前仅在服装操作任务上验证，向刚性物体操作和跨任务泛化的扩展有待验证

## 相关论文

- π0.5: 基线 VLA 模型，开源的 vision-language-action flow model
- π0: 更早的 VLA 基础模型
- π0.6*: 使用 advantage-weighted regression 的 VLA，SA 的主要对比基线
- RT-2: Vision-language-action models 用于机器人控制
- Diffusion Policy: 基于动作扩散的视觉运动策略
- Model Soups: 权重平均合并多模型的开创性工作
- DAgger: 经典的 imitation learning with dataset aggregation 方法
- AWR: Advantage-Weighted Regression，offline RL 方法
- GR-3: 服装悬挂任务的相关工作


## 原文

[[05_Papers/articles/chi0|chi0]]
