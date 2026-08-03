---
title: "RLVR"
description: "从可验证奖励中学习 (Reinforcement Learning from Verifiable Rewards) — 通过规则化奖励信号训练推理模型"
tags: [concept, ai, llm, rl, reasoning, training]
created: 2026-08-03
---

# RLVR (Reinforcement Learning from Verifiable Rewards)

RLVR 是用可自动验证的二元/稀疏奖励信号训练推理模型的 RL 方法。与 RLHF（依赖人类偏好模型）不同，RLVR 的奖励来自规则验证（数学答案匹配、代码测试通过等）。

## 核心机制

- **奖励**: 严格二元（正确/错误），无偏好排序
- **策略梯度**: 通过采样轨迹的成败反馈更新模型
- **代表算法**: GRPO、REINFORCE with baseline

## 两个核心挑战

### 1. 冷启动停滞
初始成功概率 $p_0$ 很小时，RLVR 梯度几乎为零，难以突破。逃逸时间 $\Omega(1/p_0)$，$p_0 = 10^{-3}$ 时需数万步才能看到第一个正确样本。

**缓解方案**: Tsallis 损失 ($q > 0$)，通过 $P_\theta^{-q}$ 放大低概率正确样本的梯度。

### 2. 噪声记忆（Mode Collapse）
RLVR 是 mode-seeking 的：一旦找到正确路径，倾向于反复采样类似解，推理多样性随时间收缩。

**缓解方案**: 低 $q$ 密度估计 + 温度采样 + 熵正则化。

## 与 RLHF 的对比

| | RLVR | RLHF |
|---|---|---|
| 奖励来源 | 规则/验证器 | 人类偏好模型 |
| 奖励类型 | 稀疏二元 | 连续偏好 |
| 标注成本 | 低（自动） | 高（人工） |
| 适用场景 | 数学/代码/推理 | 对话/安全对齐 |

## 相关概念

- [[01_Fundamentals/ML/Tsallis-Entropy|Tsallis Entropy]] — RLVR 冷启动问题的解决方案
- [[01_Fundamentals/ML/Cold-Start-in-RL|Cold-Start in RL]]
- [[02_AI/LLM/Chain-of-Thought-Reasoning|Chain-of-Thought Reasoning]]

## 来源

- [[05_Papers/notes/tsallis-loss-continuum|Tsallis Loss Continuum]] — RLVR 冷启动与噪声记忆的理论分析
