---
title: Flow-based VLA
description: 使用流匹配作为动作生成目标的 Vision-Language-Action 模型
tags:
  - embodied-ai
  - vla
  - flow-matching
  - robot-learning
created: 2026-07-28
---

# Flow-based VLA

Flow-based VLA 是一类使用**流匹配（Flow Matching）**作为动作生成目标的 Vision-Language-Action 模型。

## Core Idea

将机器人动作序列的生成建模为从噪声分布到动作分布的连续概率流。VLA 的动作专家（Action Expert）学习速度场，通过 ODE 采样生成平滑、多模态的动作块。

## Why Flow Matching for Actions

- **动作多模态**：同一状态-指令对可对应多种合法动作
- **连续动作空间**：流匹配天然适合连续向量输出
- **采样效率**：相比扩散模型，可用更少的去噪步数生成动作

## Architecture Pattern

1. VLM backbone 编码视觉-语言上下文
2. Action Expert 以 VLM 激活为条件，学习流匹配速度场
3. 推理时通过 5–20 步去噪生成动作块

## Training Recipe

通常结合 **Knowledge Insulation**：动作专家的梯度不回传给 VLM backbone，使 VLM 保持稳定的离散损失监督。

## Related Concepts

- [[02_AI/Generative-Models/Flow-Matching|Flow Matching]] — 通用流匹配方法
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — VLA 通用范式
- [[04_Embodied-AI/VLA/Action-Expert|Action Expert]] — 负责动作生成的子网络
- [[04_Embodied-AI/VLA/Knowledge-Insulation|Knowledge Insulation]] — 保护 VLM backbone 的训练技巧

## RL 微调

[[05_Papers/notes/pirl|πRL]] 提出针对 Flow-based VLA 的在线 RL 微调方法。核心挑战在于 Flow Matching 的确定性 ODE 采样使动作对数似然难以精确计算且缺乏探索。

### Flow-Noise

引入可学习噪声网络，将去噪过程建模为离散时间 MDP：

- 噪声幅度参数化为神经网络 $\sigma_{\theta'}(\mathbf{A}^\tau, \mathbf{o})$，在去噪过程中动态学习
- 单步转移建模为高斯：$p(\mathbf{A}^{\tau+\delta} \mid \mathbf{A}^\tau) \sim \mathcal{N}(\mu_\tau, \Sigma_\tau)$
- 整个去噪序列的精确对数概率可计算，使 Flow-based 策略可在标准 PPO 框架下优化
- 噪声网络训练时与速度场联合学习，推理时丢弃

### Flow-SDE

将确定性 ODE 转换为等价 SDE，增强探索能力：

- 利用概率流 ODE 与 SDE 的关系导出等价随机过程
- 构建**双层 MDP**：内层去噪（$\tau < 1$）+ 外层环境交互（$\tau = 1$）
- 噪声调度 $\sigma_\tau = a\sqrt{\tau/(1-\tau)}$，自动调节探索程度

**混合 ODE-SDE 采样**：每步随机选择一个去噪时间点做 SDE 探索，其余用 ODE —— 实现 $2\times$ 加速。

### 关键发现

- Flow-Noise 收敛最快，Flow-SDE 计算更高效
- 冻结 VLM backbone 限制了视觉泛化，LoRA 微调 VLM 是可行方向
- RL 主要提升动作级精细化，对跨任务语义泛化帮助有限

## 优缺点补充

- **RL 微调优势**：可超越 SFT 数据中的次优演示，提升任务成功率；
- **挑战**：流模型动作似然估计需要特殊处理；确定性采样限制探索。

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 5B 参数 Flow-based VLA，860M 参数 action expert
- [[05_Papers/articles/pi-0-6|π0]] — 提出 VLA 流模型用于通用机器人控制
- [[05_Papers/articles/pirl|piRL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models]]
