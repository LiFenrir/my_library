---
title: RECAP
description: 通过优势条件策略从经验与专家纠正中迭代训练 VLA 的离线强化学习方法
tags:
  - embodied-ai
  - robot-rl
  - vla
  - offline-rl
  - concept
created: 2026-07-28
---

# RECAP

RL with Experience and Corrections via Advantage-conditioned Policies：一套让 Vision-Language-Action（VLA）模型从真实部署经验中持续改进的通用离线 RL 流程。

## Core Idea

将演示数据、自主 rollout、专家干预三种异构数据统一纳入一个迭代离线 RL 框架：

1. **数据收集**：在真实环境中运行策略，记录带成功/失败标签的 episode， optionally 由专家进行纠正性干预。
2. **值函数训练**：用所有已收集数据训练多任务分布值函数，估计剩余步数到成功。
3. **优势条件训练**：将每个动作的优势二值化为 "Advantage: positive/negative"，作为 VLA 输入前缀进行监督学习。

重复步骤 1-3 即可持续改进策略。

## Why It Works

- **离线 RL 预训练**：先在大量演示数据上预训练 VLA 与值函数，获得通用基础。
- **利用异构数据**：演示、自主经验、专家纠正均可用于训练，不浪费任何样本。
- **避免策略梯度**：用 [[Advantage-Conditioning]] 替代 PPO，天然适配 [[Flow-Matching]] VLA。
- **可扩展**：仅通过稀疏 episode 级奖励即可训练，降低真实环境奖励工程成本。

## Key Design Choices

- **稀疏奖励**：$r_T = 0$（成功）、$-C_{\mathrm{fail}}$（失败）、其余 $-1$，使值函数学习“距成功剩余步数”。
- **二值化优势指示器**：$I_t = \mathbb{1}(A^{\pi_{\mathrm{ref}}}(\mathbf{o}_t, \mathbf{a}_t, \ell) > \epsilon_\ell)$，任务相关阈值 $\epsilon_\ell$ 控制改进强度。
- **专家纠正强制 positive**：假设人类纠正动作总是更优，将其 $I_t$ 设为 True。
- **每轮从预训练 checkpoint 微调**：避免多轮迭代漂移。

## 补充：来自 [[04_Embodied-AI/Robot-RL/RECAP|recap（已合并）]]

### 为什么需要 RECAP

- 模仿学习只能从演示中学到人类水平，无法超越
- 自主实践中收集的数据质量参差不齐
- 直接对 VLA 使用策略梯度（如 PPO）难以扩展到 flow matching/diffusion-based 大模型

### 优缺点

- **优点**：支持 flow matching/diffusion-based VLA；可利用所有历史数据（off-policy）；通过专家干预解决探索问题；在复杂长程任务上显著提升吞吐量和成功率。
- **局限**：需要训练额外的价值函数；需要定义稀疏奖励/成功标签；多轮迭代可能产生分布漂移。

## Related Concepts

- [[Advantage-Conditioning]] — RECAP 的核心策略提取机制
- [[Distributional-Value-Function]] — RECAP 中值函数的实现方式
- [[Offline-RL-for-VLA]] — RECAP 所属的 VLA 离线 RL 范式
- [[Vision-Language-Action-Model]] — RECAP 的改进对象
- [[Classifier-Free-Guidance]] — 可用于 RECAP 推理时进一步锐化策略

## Papers

- [[pi-0-6]] — $\pi^*_{0.6}$: a VLA That Learns From Experience
