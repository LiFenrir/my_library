---
title: "How Fast Should a Model Commit to Supervision? Training Reasoning Models on the Tsallis Loss Continuum"
description: "在 Tsallis 损失连续体上训练推理模型，平衡监督承诺与探索。"
tags: ["强化学习", "Reasoning", "RLVR", "Tsallis Loss"]
created: 2026-07-15
---

# How Fast Should a Model Commit to Supervision? Training Reasoning Models on the Tsallis Loss Continuum

## 基本信息
- **作者**: Chu-Cheng Lin, Eugene Ie
- **机构**: Google
- **链接**: 
- **发表**: 2026-04-28
- **代码**: 未公开

## 研究背景与动机

推理模型通过生成潜在计算轨迹（思维链、证明草图、搜索轨迹）来有效解决复杂任务。RLVR（Reinforcement Learning from Verifiable Rewards）是训练此类模型的常用方法，但面临两个核心问题：

1. **冷启动停滞**：当初始成功概率 $p_0$ 很小时，RLVR 难以取得进展
2. **噪声记忆**：RLVR 是 mode-seeking 的，推理能力边界可能随训练变窄，限制样本多样性

现有方法如 Rao-Blackwellized rewards 虽确保非零梯度，但仅降低梯度方差而未解决逃逸速度瓶颈。指令工程虽可提供足够结构，但依赖任务特定提示。

![[99_Attachments/papers/images/tsallis-loss-continuum/99fbc2e100f586ed6cb23f29b40ea97dfa5ea3480b63be747e23f7f44bffb56e.jpg]]

## 核心方法: $J_Q$ Loss Continuum

### Tsallis $q$-对数
使用 Tsallis $q$-对数定义损失族：

$$
\log_q(u) = \frac{u^{1-q} - 1}{1-q}, \quad 0 < u \leq 1
$$

### $J_Q$ 损失族

$$
J_Q(\theta, q) = \mathbb{E}_{(x^*, y^*) \sim \mathcal{D}} [-\log_q(P_\theta)]
$$

其中 $P_\theta = p_\theta(y^* | x^*)$ 为成功概率。

**两个端点**：
- **$q=0$（Exploitation Pole）**：$J_0 = \mathbb{E}[1 - P_\theta]$，等价于 RLVR
- **$q=1$（Density-Estimation Pole）**：$J_1 = \mathbb{E}[-\log P_\theta]$，对数边缘似然

### Commitment 机制
所有成员共享相同的逐样本梯度方向，仅通过标量放大 $P_\theta^{-q}$ 区分：
- **高 $q$**：快速解决歧义（冷启动逃逸快），但记忆噪声
- **低 $q$**：解决噪声（鲁棒过滤），但逃逸慢至 $\Omega(1/p_0)$

![[99_Attachments/papers/images/tsallis-loss-continuum/fd5235b385a4bb8afbf8ff111c745e96bfb5dd6efec1f509b79720fe5bb1084d.jpg]]

### 两种梯度估计器

**GARL（Gradient-Amplified RL）**：
- 从先验采样轨迹，放大 RL 梯度
- 低方差，但混合不良推理到梯度中
- 冷启动时必需（后验采样无轨迹）

**PAFT（Posterior-Attenuated Fine-Tuning）**：
- 从答案一致的后验近似采样，运行标准 SFT
- 梯度语义一致，但有重采样噪声
- 暖启动时更稳定

两者偏差均为 $O(q / M P_\theta^{q+1})$。

## 实验结果

**基准**：FinQA, HotPotQA, MuSiQue（严格精确匹配奖励）

**主要发现**：
- **冷启动**：GARL 在 $q=0.75$ 显著缓解冷启动停滞，在 GRPO 完全失败处逃逸
- **暖启动**：
  - FinQA：GARL $q=0.25$ 领先（38.7 vs. GRPO 26.9）
  - HotPotQA：PAFT $q=0.75$ 最佳（47.9 vs. GRPO 33.5，+14.4）
  - MuSiQue：PAFT $q=0.75$ 最佳（22.4 vs. GRPO 15.8）

## 理论分析

- **逃逸速度**：Exploitation pole 需要 $\Omega(1/p_0)$ 时间逃逸；Density-estimation pole 在 $\Theta(\log(1/p_0))$ 内逃逸
- **损失景观**：固定样本的 $q$-损失 $\ell_q = (1 - P_\theta^{1-q})/(1-q)$，$q=0$ 时有界 $[0,1]$，$q=1$ 时无界
- **极小值**：由 escort 分布 $\theta_j^* \propto \alpha_j^{1/q}$ 给出

## 核心贡献

1. **$J_Q$ 损失族**：通过 Tsallis $q$-对数在 RLVR 和密度估计之间插值
2. **Commitment 概念**：训练时探索-利用权衡的量化，控制冷启动逃逸速度
3. **两种实用估计器**：GARL 和 PAFT，分别适用于冷启动和暖启动场景
4. **实证验证**：在三个推理基准上验证，最佳方法比 GRPO 提升 +6.6 到 +14.4 点

## 个人思考

- **理论深度**：将冷启动问题形式化为梯度逃逸速度问题是优雅的，$P_\theta^{-q}$ 放大机制提供了清晰的直觉
- **实用性**：GARL/PAFT 的选择取决于训练阶段，这种阶段性策略在实际训练中很有价值
- **局限**：仅在问答任务上验证，未涉及代码生成或数学证明等更复杂的推理任务
- **扩展方向**：探索自适应 $q$ 调度策略；结合课程学习动态调整 commitment


## 原文

[[05_Papers/articles/tsallis-loss-continuum|tsallis-loss-continuum]]
