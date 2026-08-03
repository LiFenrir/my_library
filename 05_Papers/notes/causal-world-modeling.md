---
title: "Causal World Modeling for Robot Control"
description: "利用因果世界模型进行机器人控制，结合自回归扩散与视频预测学习可泛化策略。"
tags: ["世界模型", "因果建模", "机器人控制", "自回归扩散", "视频预测", "逆动力学", "Robbyant"]
created: 2026-07-15
---

# Causal World Modeling for Robot Control

## 基本信息

- **作者**: Lin Li*, Qihang Zhang*†, Yiming Luo*, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, Yinghao Xu‡
- **机构**: Robbyant
- **链接**: https://arxiv.org/abs/2601.21998
- **项目页**: https://technology.robbyant.com/lingbot-va
- **代码**: https://github.com/robbyant/lingbot-va
- **模型**: https://huggingface.co/robbyant/lingbot-va
- **发表**: arXiv 2025

## 研究背景与动机

### VLA 的核心问题：表示纠缠
现有 Vision-Language-Action (VLA) 模型采用前馈范式，将当前观测映射到动作序列，要求单一网络同时学习：
- 视觉场景理解
- 物理动力学
- 运动控制

这种**表示纠缠**导致：
- 样本效率低下
- 泛化能力受限
- 依赖模式匹配而非对物理动力学的原理性理解

### 现有世界模型方法的局限
1. **反应性差距**: 块/开环生成无法融入实时反馈
2. **长期记忆有限**: 块级生成在长时间范围内引入不一致性
3. **因果性缺失**: 段内双向注意力允许未来 token 影响过去预测，违背物理现实的因果结构

### 核心洞察
物理世界本质上是**因果和自回归**的：当前状态仅依赖于过去。这启发了 LingBot-VA 的自回归世界建模方法。

## 核心方法

### 问题分解
将机器人操作分解为两个阶段：

**Stage 1 - 视觉动力学预测**:
$$o_{t+1} \sim p_\theta(\cdot | o_{\leq t})$$

**Stage 2 - 逆动力学**:
$$a_t \sim g_\psi(\cdot | o_t, o_{t+1})$$

这种分解使 Stage 1 能利用大规模视频数据学习物理先验，而 Stage 2 仅需机器人演示将视觉预测转化为可执行动作。

### LingBot-VA 架构

![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig1_overview_a.jpg]]
![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig1_overview_b.jpg]]
![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig1_overview_c.jpg]]

**三大核心设计**:

#### 1. 自回归视频-动作世界建模

![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig2_framework.jpg]]

- **自回归生成**: 每个步骤预测下一个包含 K 帧的视频块
- **块内并行**: 块内 token 通过双向注意力并行生成
- **跨块因果**: 保持跨块因果结构，支持闭环校正

**视频-动作状态编码**:
- 视觉观测通过因果视频 VAE 压缩为隐变量 token: $z_t = E(o_t | o_{<t})$
- 动作向量通过轻量 MLP 投影为 token 嵌入
- 时序下采样因子 $\tau = 4$，每帧视频关联 $\tau$ 个连续动作
- 统一序列: $[z_t, a_{t,1}, a_{t,2}, ..., a_{t,\tau}, z_{t+1}, ...]$

**逆动力学动作解码**:
$$a_{t:t+K-1} \sim g_\psi(\cdot | \hat{z}_{t+1:t+K}, z_{\leq t}, a_{<t})$$

#### 2. Mixture-of-Transformers (MoT) 架构

- **双流失散架构**: 
  - 视频流: Wan2.2-5B 初始化，维度 $d_v = 3072$，30 层
  - 动作流: 同深度，维度 $d_a = 768$（4× 更小），约 350M 参数
  - 总参数量: **5.3B**

- **跨模态融合**: 
  - 每层视频和动作流独立计算 QKV
  - 动作 token 投影到视频维度参与联合自注意力
  - 残差连接保持动作特定表示

**动作网络初始化策略**:
- 随机初始化 → 不稳定，收敛慢
- 直接复用视频权重 → 次优
- **本文方法**: 插值预训练视频权重 + 缩放因子 $\alpha = \sqrt{d_v / d_a}$ → 最稳定、收敛最快

![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig7_init_a.jpg]]
![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig7_init_b.jpg]]
![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig7_init_c.jpg]]

#### 3. 噪声历史增强 (Noisy History Augmentation)

**关键洞察**: 动作预测不需要像素级完美的视频表示，可以依赖鲁棒的语义结构。

**训练时**:
$$\tilde{z}_{\leq t} = \begin{cases} (1 - s_{\text{aug}})\epsilon + s_{\text{aug}} z_{\leq t}, & p = 0.5, \quad s_{\text{aug}} \in [0.5, 1] \\ z_{\leq t}, & p = 0.5 \end{cases}$$

**推理时**: 视频 token 只需去噪到 $s = 0.5$（而非 $s = 1.0$），去噪步数减半。

#### 4. 异步推理管道

![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig4_async_a.jpg]]
![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig4_async_b.jpg]]

**问题**: 朴素异步实现依赖过时的视觉预测，导致开环退化。

**解决方案 - 前向动力学模型 (FDM) 接地**:
1. 使用最新真实反馈 $z_{t-1}$
2. "想象"执行动作 $a_t$ 后的视觉状态 $z_t$
3. 用反馈接地的预测替代陈旧预测
4. 强制模型在预测 $z_{t+1}$ 前重新与环境反馈对齐

**推理配置**:
- 视频 token: Euler 求解器，3 步（积分到 $s = 0.6$）
- 动作 token: 10 步（积分到 $s = 1.0$）
- 视频 CFG: 5.0，动作 CFG: 1.0

### 训练目标

**统一目标**: $\mathcal{L} = \mathcal{L}_{\text{dyn}} + \lambda \mathcal{L}_{\text{inv}}$

**视觉动力学损失**:
$$\mathcal{L}_{\text{dyn}} = \mathbb{E}_{t,s,z_{t+1},\epsilon} \left[ \| v_\theta(z_{t+1}^{(s)}, s, \tilde{z}_{\leq t}, a_{<t} | c) - \dot{z}_{t+1}^{(s)} \|^2 \right]$$

**逆动力学损失**:
$$\mathcal{L}_{\text{inv}} = \mathbb{E}_{t,s,a_t,\epsilon} \left[ \| v_\psi(a_t^{(s)}, s, \tilde{z}_{\leq t+1}, a_{<t} | c) - \dot{a}_t^{(s)} \|^2 \right]$$

**前向动力学损失**（后训练）:
$$\mathcal{L}_{\text{fdm}} = \mathbb{E}_{t,s,\hat{z}_{t+1},\epsilon} \left[ \| v_\psi(\tilde{z}_{t+1}, s, z_t, a_t, \tilde{z}_{<t}, \hat{a}_{<t} | c) - \dot{z}_{t+1}^{(s)} \|^2 \right]$$

### 训练细节

**预训练**:
- 数据: ~16K 小时机器人操作数据（Agibot, RoboMind, InternData-A1, OXE, UMI, RoboCOIN）
- 规模: 1.4T tokens
- 优化器: AdamW，峰值学习率 $1 \times 10^{-4}$
- 精度: bfloat16 混合精度
- 动作维度: 30（双臂：7 EEF + 7 joints + 1 gripper）× 2

**后训练**:
- 仅需 **50 次演示** 即可有效部署
- 学习率: $1 \times 10^{-5}$，3K 步
- 或快速选项: $1 \times 10^{-4}$，1K 步

## 实验结果

### 真实世界部署

![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig5_realworld.jpg]]
![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig6_tasks.jpg]]

在 6 个真实世界任务上评估（仅需 50 次演示后训练）：

| 类别 | 任务 | 相比 π₀.₅ 提升 |
|------|------|---------------|
| **长程任务** | 做早餐、捡螺丝 | >20% |
| **精度任务** | 插入管子、拆包裹 | >20% |
| **可变形物体** | 叠衣服、叠裤子 | >20% |

**关键观察**:
1. **长程任务**: 视频-动作世界模型具有强时序记忆能力
2. **精度任务**: 统一隐空间设计实现视觉感知与运动控制的紧密耦合
3. **可变形物体**: 生成视频未来提供丰富的物体动力学预测信号

### 仿真评估

#### RoboTwin 2.0（双臂操作，50 任务）

| 方法 | Easy | Hard |
|------|------|------|
| π₀ | 65.9% | 58.4% |
| π₀.₅ | 82.7% | 76.8% |
| Motus | 88.7% | 87.0% |
| **LingBot-VA** | **92.9%** | **91.6%** |

- **Horizon=3** 任务提升最显著: +8.2% (Easy), +9.1% (Hard)
- 表明自回归机制有效维持长程时序记忆

#### LIBERO（4 个任务套件）

| 方法 | Spatial | Object | Goal | Long | Avg |
|------|---------|--------|------|------|-----|
| π₀ | 96.8% | 98.8% | 95.8% | 85.2% | 94.1% |
| X-VLA | 98.2% | 98.6% | 97.8% | 97.6% | 98.1% |
| **LingBot-VA** | **98.5%** | **99.6%** | **97.2%** | **98.5%** | **98.5%** |

- 在 LIBERO-Object (99.6%) 和 LIBERO-Long (98.5%) 上达到 **SOTA**
- 平均成功率 98.5%，超越所有基础 VLA 模型

### 消融实验

#### 异步 vs 同步
- 成功率相当
- 异步方法 **2× 更快**（通过并行预测和执行）

#### 预训练 LingBot-VA vs WAN
- LingBot-VA: 92.1% (Easy), 91.1% (Hard)
- WAN 微调: 80.6% (Easy), 显著更低
- 联合视频-动作预训练提供丰富的视觉-运动先验

#### 自回归 vs 双向
- 朴素异步（无 FDM 接地）: 74.3%（严重退化）
- FDM 接地异步: 90.4%
- 证明 FDM 接地对闭环控制至关重要

### 样本效率

![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig8_sample_efficiency.jpg]]

- **10 次演示**: 
  - Make Breakfast: +15.6% 进度分 vs π₀.₅
  - RoboTwin Easy: +10.3%
- 视频-动作世界模型设计提供丰富的视觉先验作为隐式正则化

### 时序记忆

![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig9_memory.jpg]]

设计两个显式记忆任务：
1. **擦盘子**: 必须恰好擦 6 次（需要计数）
2. **搜索盒子**: 两个盒子只有一个有方块，找到空盒后需记住并搜索另一个

结果：LingBot-VA 显著超越 π₀.₅，归因于：
- 训练时 Teacher Forcing 条件于完整历史
- 推理时 KV Cache 自然保留所有历史信息

### 泛化能力

![[99_Attachments/papers/images/causal-world-modeling/lingbot_fig10_generalization_a.jpg]]

- **新物体泛化**: 训练时单物体，测试时不同形状和纹理
- **空间泛化**: 训练时固定位置，测试时随机放置（含分布外区域）

LingBot-VA 在两种泛化上都表现更强，因为世界模型通过视频预测学习可迁移的视觉表示。

## 关键贡献

1. **自回归视频-动作世界建模**: 统一视觉动力学预测和动作推断的因果自回归框架
2. **MoT 架构 + 异步执行**: 双流失散架构配合部分去噪策略实现高效控制
3. **SOTA 长程和精度性能**: RoboTwin 92.9%，LIBERO 98.5%，真实世界 >20% 提升
4. **数据效率**: 仅需 50 次演示即可后训练部署
5. **开源**: 代码、模型权重、检查点全部公开

## 与 DreamZero (WAM) 的对比

| 特性 | DreamZero (NVIDIA) | LingBot-VA (Robbyant) |
|------|-------------------|----------------------|
| **骨干模型** | Wan2.1-I2V-14B | Wan2.2-5B |
| **总参数量** | 14B | 5.3B |
| **架构** | 自回归 DiT，共享去噪 | MoT 双流失散 |
| **视频-动作关系** | 联合去噪 | 视频先预测，动作后解码 |
| **噪声调度** | Flash: 解耦视频/动作 | 噪声历史增强 |
| **推理速度** | 7Hz (GB200) | 异步 2× 加速 |
| **训练数据** | ~500h 自采 + DROID | ~16Kh 聚合公开数据 |
| **后训练数据** | 12-40h 每任务 | 50 次演示 |
| **核心优势** | 零样本泛化、跨本体迁移 | 长程记忆、样本效率 |

**共同点**:
- 都基于自回归视频扩散
- 都用 Flow Matching
- 都用 Teacher Forcing
- 都强调闭环控制
- 都继承 Wan 视频模型先验

## 局限性与未来工作

1. **计算开销**: 视频 token 生成仍是瓶颈
2. **多模态感知**: 未融入触觉、力觉、音频
3. **视频压缩**: 更高效的压缩方案可减少计算
4. **长上下文**: 当前 10K tokens，可进一步扩展

## 个人评价

**重要性**: ★★★★☆
- 系统性地论证了因果自回归世界模型相对于 VLA 的优势
- 在多个基准上达到 SOTA，且仅需极少后训练数据
- 完全开源（代码+模型+权重），利于社区复现和改进

**与 DreamZero 的关系**:
这两篇论文（2601.21998 和 2602.15922）几乎同期出现，代表了世界动作模型 (WAM) 方向的两大并行进展：
- **DreamZero** 强调零样本泛化和跨本体迁移，使用更大模型 (14B)
- **LingBot-VA** 强调长程记忆和样本效率，使用更轻量模型 (5.3B)

两者共同验证了：**视频世界建模 + 自回归扩散 + 闭环控制** 是机器人学习的一个有前景的新范式，与 VLA 形成有力竞争。

**可改进方向**:
- 探索更小的视频骨干模型以实现边缘部署
- 结合 System 2 规划器处理复杂长程任务
- 融入多模态感知增强接触动力学理解

## 相关项目

- [[06_Projects/external/lingbot/lingbot-va|LingBot-VA 项目笔记]]
- 项目页：https://technology.robbyant.com/lingbot-va
- 代码：https://github.com/robbyant/lingbot-va
- 模型：https://huggingface.co/robbyant/lingbot-va

## 相关论文

- [DreamZero](https://arxiv.org/abs/2602.15922) - 同期 WAM 工作 (NVIDIA)
- [π₀](https://arxiv.org/abs/2410.24164) / [π₀.₅](https://arxiv.org/abs/2410.24164) - VLA baseline
- [GR00T N1](https://arxiv.org/abs/2503.14734) - NVIDIA humanoid VLA
- [Motus](https://arxiv.org/abs/2502.16660) - 视频-动作联合生成
- [UWM](https://arxiv.org/abs/2502.16660) - 统一世界模型
- [Wan2.1/Wan2.2](https://github.com/Wan-Video/Wan2.1) - 视频生成骨干


## 原文

[[05_Papers/articles/causal-world-modeling|causal-world-modeling]]
