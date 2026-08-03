---
title: "ARM: Advantage Reward Modeling for Long-Horizon Manipulation"
description: "通过优势奖励模型提升长程机器人操作任务的成功率。"
tags: ["具身智能", "Reward Modeling", "Long-Horizon Manipulation"]
created: 2026-07-15
---

# ARM: Advantage Reward Modeling for Long-Horizon Manipulation

## 基本信息
- **作者**: Yiming Mao, Zixi Yu, Weixin Mao, Yinhao Li, Qirui Hu, Zihan Lan, Minzhao Zhu, Hua Chen
- **机构**: LimX Dynamics, Beijing University of Posts and Telecommunications, Zhejiang University
- **链接**: https://aiming1998.github.io/ARM
- **发表**: arXiv preprint, 2026 (arXiv:2604.03037)
- **代码**: 未开源

## 研究背景与动机

### 问题陈述
- **VLA 模型依赖模仿学习 (IL) 的局限**: 现有 VLA 方法严重依赖 IL，需要大规模数据集，且人类演示中的次优性和噪声在长程任务中阻碍策略收敛。
- **强化学习 (RL) 的奖励瓶颈**: 长程操作任务中，稀疏奖励难以提供有效的信用分配信号，而密集奖励的获取成本高昂。
- **现有进度奖励方法的缺陷**:
  - **零样本 VLM 标注**: 不可靠、成本高，缺乏空间几何基础，奖励信号非单调振荡。
  - **单调性假设**: 将进度等同于时间顺序，无法刻画真实的非线性操作错误（如回溯、恢复）。
  - **粗粒度子任务划分**:  无法捕捉长程任务中关键的恢复和纠正行为。 

### 核心洞察
将奖励建模从难以量化的**绝对进度** (absolute progress) 转向更直观的**相对优势** (relative advantage)。相对优势提供了一个任务无关、简洁且可扩展的标注原语。

## 核心方法

### 1. 三态优势标注策略 (Tri-state Advantage Labeling)

将连续进度标注简化为三种离散状态，显著降低认知负荷并提高标注一致性：

![[99_Attachments/papers/images/arm/a137d11a7c15a8c792198125314882646c2137f29ea9f515e41daf764e28be62.jpg]]
*图3：三态标注策略示意图*

| 标签 | 符号 | 含义 |
|------|------|------|
| **Progressive** | +1 | 状态有效推进任务目标 |
| **Regressive** | -1 | 状态偏离目标、遇到错误或失败 |
| **Stagnant** | 0 | 无实质进展，对应等待或空闲行为 |

**优势**:
- 任务无关 (task-agnostic)，适用于异构和碎片化数据
- 人类标注效率提升 **2.5x** (250 vs 100 samples/8h)
- 自动化标注效率提升 **>133x** (>400,000 vs 3,000 samples/8h)

### 2. Advantage Reward Model (ARM)

采用 **MIMO (Multi-Input Multi-Output)** 时序 Transformer 架构，替代传统的 MISO 模型：

![[99_Attachments/papers/images/arm/3d29758dc6bb752d7b804e40dd4121fd279578bfabb21a8fd096887137cf7476.jpg]]
*图1A：Advantage Reward Model (ARM) 架构*

![[99_Attachments/papers/images/arm/d2355b87001367128eaec04fc6330e54c937e420b86bb76884e892124ebbd749.jpg]]
*图2：MISO vs MIMO 架构对比*

#### 输入
- **视觉特征**: CLIP ViT-B/32 提取
- **本体感知状态**: 机器人关节位置和夹爪状态
- **任务指令**: 语言目标编码

#### 双头学习目标

**Head 1: 多帧优势分类 (Interval Head)**
- 预测连续隐藏状态间的优势转换 $\Delta \hat{y} \in \{-1, 0, +1\}$
- 使用交叉熵损失 $\mathcal{L}_{\text{int}}$
- 将奖励估计从连续回归转化为离散分类，增强对噪声的鲁棒性

**Head 2: 任务完成预测 (Completion Head)**
- 预测当前观测是否为成功终止状态
- 使用 Focal Loss 处理类别不平衡:
  $$
  \mathcal{L}_{\text{succ}} = \text{FocalLoss}(C_t, \mathbb{1}[P_t \geq 1 - \epsilon])
  $$

**总目标**:
$$
\mathcal{L}_{\text{ARM}} = \lambda_{\text{int}} \mathcal{L}_{\text{int}} + \lambda_{\text{succ}} \mathcal{L}_{\text{succ}}
$$

### 3. 全局进度重建 (Global Progress Reconstruction)

将离散的区间优势预测合成为连贯的全局进度曲线：

![[99_Attachments/papers/images/arm/a74755f7e9129078ed4c825a49b6657d84cf28504012e509526a9c541142fe8a.jpg]]
*图1B：Global Progress Reconstruction 流程*

1. **并行推理**: MIMO 架构直接预测序列，非重叠片段可并行处理
2. **序列对齐**: 终端片段不足窗口大小时使用尾帧复制填充
3. **进度生成**: 以任务完成信号 $C_t$ 为锚点，通过累积 $\Delta \hat{y}$ 重建密集进度值 $P_t$

### 4. Advantage-Weighted Behavior Cloning (AW-BC)

![[99_Attachments/papers/images/arm/5181f7f72dee705fbb20b091194c6a2d582ad6f173f237199a68a934e4496fcb.jpg]]
*图1C：Advantage-Weighted Behavior Cloning (AW-BC) 框架*

#### 长度自适应增益 (Length-adaptive Gain)
为缓解异构演示中的长度偏差，引入自适应缩放：
$$
\Delta G_t = (P_{t+H} - P_t) \cdot \frac{L_{\text{seq}}}{\bar{L}}
$$
其中 $L_{\text{seq}}$ 为当前回合长度，$\bar{L}$ 为数据集平均长度。

#### 统计加权
基于批次增益分布计算重要性权重：
$$
\tilde{w}_i = \text{clamp}\left(\frac{\Delta G_i - b_{\text{lower}}}{b_{\text{upper}} - b_{\text{lower}} + \epsilon}, 0, 1\right)
$$
其中 $b_{\text{lower}} = \mu - 2\sigma$, $b_{\text{upper}} = \mu + 2\sigma$。

#### 优化目标
$$
\mathcal{L}_{\text{AW-BC}}(\theta) = \mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ -\tilde{w}(s,a) \log \pi_\theta(a|s) \right]
$$

## 关键创新点

1. **相对优势替代绝对进度**: 通过估计状态间的相对优势而非绝对进度，自然支持回溯和恢复行为，摆脱任务特定的启发式设计。

2. **三态标注策略**: 将昂贵的连续标注简化为三种离散状态，在降低认知负荷的同时保持高保真监督信号。

3. **MIMO 时序架构**: 多输入多输出设计允许模型在单次前向传播中预测多个优势转换，推理速度提升 **3.6x** (14.1 vs 3.9 it/s)。

4. **AW-BC 算法**: 通过长度自适应增益和统计归一化，有效过滤次优样本并优先学习高价值恢复行为。

## 实验结果

### 实验设置
- **任务**: 长程双臂毛巾折叠 (8 阶段: 提取→放置→展平→纵向折叠×2→横向折叠×2→放入收纳盒)
- **硬件**: AgileX ALOHA 双臂遥操作系统
- **数据集**: 972 条演示 (20 小时)，809 条专家 + 163 条 DAgger 纠错
- **策略基础**: GR00T-N1.5-3B

![[99_Attachments/papers/images/arm/e47bf1c9c333366e83c4d05098c2fdc3cab437ceb365acdead35483fbe9af4e6.jpg]]
*图4：长程毛巾折叠任务概览*

### 奖励模型性能 (Table 1)

| Metrics | SARM | ARM (Ours) |
|---------|------|------------|
| MSE ↓ | 0.0059 | **0.0014** |
| Success ID - Standard | 83.3% | **100.0%** |
| Success ID - Failure | 91.6% | **100.0%** |

![[99_Attachments/papers/images/arm/8ab91127c7ceb64390d668389d9bcbf6907ed97c08c3a5de3365962a66b63bfe.jpg]]
*图5：进度重建的定性对比。SARM 难以处理非单调行为，而 ARM 能重建平滑、高保真的进度曲线*

### 下游策略性能 (Table 2)

| Method | Success Rate (%) | Task Throughput (Ep/hr) | Folding Precision |
|--------|-----------------|------------------------|-------------------|
| BC-Baseline (GR00T N1.5) | 62.1 | 18 | 2.2 |
| RA-BC (GR00T + SARM) | 78.5 | 24 | 2.7 |
| **AW-BC (GR00T + ARM)** | **99.4** | **32** | **3.6** |

### 消融实验 (Table 5)

| Method | Task Seg. | Tri-state | RA-BC | AW-BC | Success Rate (%) |
|--------|-----------|-----------|-------|-------|-----------------|
| SARM | ✓ | - | ✓ | - | 78.5 |
| ARM | - | ✓ | ✓ | - | 92.3 (+13.8%) |
| **ARM** | - | ✓ | - | **✓** | **99.4 (+7.1%)** |

- 三态标注 vs 子任务分段: **+13.8%**
- AW-BC vs RA-BC: **+7.1%**
- 完整框架 vs SARM: **+20.9%**

![[99_Attachments/papers/images/arm/d500a5cdd861d2d6663338596e452f6e878413ba0b5f7fe30f715bc887a4017c.jpg]]
![[99_Attachments/papers/images/arm/c670e037d9247dde9caca5434dcf4e25e299d41a317943bb50cbdd90afb63fb1.jpg]]
*图6：进度重建的定性对比。三态方法生成更平滑、一致的密集进度信号，相比手动分段和 VLM 方法的阶梯曲线*

### 推理效率 (Table 4)

| Method | Architecture | Throughput (it/s) |
|--------|-------------|-------------------|
| Qwen3-VL | MISO | 1.03 |
| SARM Baseline | SISO | 3.9 |
| **ARM (Ours)** | **MIMO** | **14.1** |

## 个人思考与启发

1. **"相对优于绝对"的范式洞察**: ARM 的核心贡献在于识别出绝对进度标注的根本困难——它需要任务特定的启发式定义。相对优势则是一个更通用、更直观的原语。这种"相对化"的思想在机器人学习中有广泛适用性：当绝对度量困难时，考虑相对比较。

2. **三态标注的实践智慧**: 将连续问题离散化为三分类，是一种在标注成本和学习精度之间寻找最优平衡的策略。+1/0/-1 的粒度刚好足够区分"好/平/坏"，又不至于引入标注噪声。这与人类认知中的"趋近-回避"机制也更为对齐。

3. **MIMO 架构的效率优势**: 传统滑动窗口方法存在大量冗余计算。MIMO 通过共享特征表示摊销多输出的计算成本，这种"一次编码、多次预测"的设计对实时机器人应用至关重要。

4. **AW-BC 的理论连接**: 论文将 AW-BC 与 AWR 建立了数学联系，将 ARM 视为学习到的 Critic。这揭示了离线 RL 与模仿学习之间的深层联系——当环境奖励不可用时，学习一个奖励模型即可恢复 RL 的优势。

5. **局限与方向**:
   - 论文仅在毛巾折叠任务上验证，更广泛的接触丰富任务（如装配、烹饪）上的泛化能力有待验证
   - 三态标注虽然高效，但对于需要细粒度区分的微妙操作（如力控），可能损失部分信息
   - 全局进度重建依赖任务完成锚点，在开放式任务（无明确终止状态）中可能失效
   - 未来可探索将 ARM 与在线 RL 结合，实现策略的持续自改进

## 相关论文

- SARM — Stage-aware Reward Modeling，ARM 的主要对比基线
- VLAC — 同样使用区间增益预测，但假设进度与时间正相关
- GR00T-N1 — ARM 策略训练的基础 VLA 模型
- AWR — Advantage-Weighted Regression，AW-BC 的理论基础
- AWAC — Advantage-Weighted Actor-Critic
- IQL — Implicit Q-Learning
- DAgger — 数据集增强策略，用于生成纠错轨迹
- Robo-Dopamine — 基于 hop 的进度奖励机制
- ReWiND — 基于视频回退模拟回归的方法
- π0 — Flow-matching VLA 模型
- OpenVLA — 开源 VLA 模型


## 原文

[[05_Papers/articles/arm|arm]]

