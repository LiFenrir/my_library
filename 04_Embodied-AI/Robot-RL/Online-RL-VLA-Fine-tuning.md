---
title: "Online RL for VLA Fine-tuning"
description: "通过在线强化学习微调 Vision-Language-Action 模型的方法、挑战与最佳实践"
tags: [concept, embodied-ai, vla, rl, fine-tuning, online-learning]
created: 2026-08-03
---

# Online RL for VLA Fine-tuning

在线 RL 微调是 VLA 训练的新范式：预训练 → SFT → RL，通过环境交互优化策略在真实部署场景中达到超越演示水平的执行精度。

## 挑战

1. **对数似然难计算**: Flow-based VLA 使用 ODE 确定性采样，动作概率无闭式表达
2. **表示维度高**: 十亿参数 VLA 的内部嵌入直接做 RL 计算和样本成本过高
3. **信用分配**: 高频控制（50Hz）下单步 RL 很难判断哪一步贡献了最终成功

## 三种技术路线

### 1. 全模型 RL（RECAP, PPO）
直接微调全部/部分 VLA 参数，效果最好但计算开销大。

### 2. 表示瓶颈 + 轻量 RL（RLT）
- 冻结 VLA，训练 encoder-decoder 将高维嵌入压缩为 RL token
- 在紧凑的 RL token 上运行 actor-critic
- 动作空间中 actor 以 VLA 参考动作为条件做局部精炼

### 3. Flow-Noise / Flow-SDE（πRL）
- Flow-Noise: 引入可学习噪声网络，将去噪过程建模为离散 MDP
- Flow-SDE: ODE→SDE 转换，双层 MDP 耦合去噪与环境交互
- 实现精确对数似然估计，使 Flow-based VLA 可用标准 RL

## 关键实践

| 技术 | 作用 |
|------|------|
| Action Chunking | 缩短有效决策时域（$C=10$ 将 50Hz 压缩为 5 步/秒） |
| BC 正则化 | 约束策略不偏离 VLA 先验太远 |
| Reference Action Dropout | 防止 actor 简单复制，保持独立探索 |
| 关键阶段聚焦 | 仅在精度瓶颈阶段应用 RL，其他阶段用 base VLA |
| off-policy replay | 异步更新，update-to-data ratio $5\times$ |

## 相关概念

- [[04_Embodied-AI/VLA/Flow-based-VLA|Flow-based VLA]] — Flow-Noise/Flow-SDE 技术细节
- [[04_Embodied-AI/Robot-RL/rl-token|RL Token]] — RLT 方法的实现

## 来源

- [[05_Papers/notes/pirl|πRL]] — Flow-Noise 与 Flow-SDE 方法
- [[05_Papers/notes/rl-token-bootstrapping|RL Token]] — RL Token bootstrapping 方法
