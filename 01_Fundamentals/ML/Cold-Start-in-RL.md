---
title: "Cold-Start in RL"
description: "强化学习中因初始成功概率过低导致的梯度消失与逃逸速度瓶颈"
tags: [concept, ml, rl, cold-start, exploration]
created: 2026-08-03
---

# Cold-Start in RL

RL 冷启动问题：当初始策略在稀疏奖励任务上的成功概率 $p_0$ 极低时，策略梯度近似为零，模型无法通过探索积累正向信号。

## 形式化

策略梯度 $\nabla_\theta J = \mathbb{E}[\nabla_\theta \log \pi_\theta(a|s) \cdot A(s,a)]$。

当 $p_0 \ll 1$ 时：
- 几乎所有轨迹的 advantage 为零或负
- 正确轨迹的梯度被负样本淹没
- 逃逸时间 $\Omega(1/p_0)$，呈超线性增长

## Mitigation 策略

| 策略 | 机制 | 适用场景 |
|------|------|---------|
| 课程学习 | 从简单任务逐步进阶 | 任务可分难度 |
| 演示预热 (SFT warmup) | 先模仿专家再 RL | 有少量演示数据 |
| 奖励塑形 | 添加密集中间奖励 | 可定义子目标 |
| Tsallis 损失 ($q>0$) | 梯度放大低概率事件 | 推理模型训练 |
| 熵正则化 | 强制策略保持探索 | 连续控制 |

## Tsallis 损失的解决方案

使用 $q$-对数替代标准对数：梯度放大因子 $P_\theta^{-q}$，使低概率正确样本获得超比例梯度权重。$q=0.75$ 可在 GRPO 完全失败处实现逃逸。

## 相关概念

- [[01_Fundamentals/ML/Tsallis-Entropy|Tsallis Entropy]] — 冷启动的梯度放大解法
- [[02_AI/LLM/RLVR|RLVR]] — RLVR 中冷启动的具体表现
- [[01_Fundamentals/ML/Behavior-Cloning|Behavior Cloning]] — 演示预热策略

## 来源

- [[05_Papers/notes/tsallis-loss-continuum|Tsallis Loss Continuum]] — 冷启动逃逸速度的理论分析
