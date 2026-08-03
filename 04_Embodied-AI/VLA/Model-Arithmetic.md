---
title: Model Arithmetic
description: 在权重空间合并多个互补策略以缓解训练数据覆盖不足导致的模型偏置
tags:
  - embodied-ai
  - model-merging
  - robot-learning
  - vla
  - concept
created: 2026-07-30
---

# Model Arithmetic

Model Arithmetic（MA）是一种 **weight-space model merging** 策略：将分别在互补数据子集上训练得到的策略检查点按可学习的系数插值，合成一个覆盖更多模式统一策略，从而缓解训练数据稀疏导致的 $Q_{\mathrm{model}}$ 偏置。

## Why

专家 demonstration 成本高昂，$P_{\mathrm{train}}$ 往往只能覆盖高维解流形的局部。传统做法是继续收集数据直到 $P_{\mathrm{train}} \approx P_{\mathrm{real}}$，但在真实机器人上不可扩展。MA 用同一批数据的不同划分训练多个策略，再通过合并权重把它们的知识“拼”起来。

## Core Idea

给定训练数据划分 $\{\mathcal{D}_1, \dots, \mathcal{D}_n\}$，分别训练策略参数 $\{\theta_1, \dots, \theta_n\}$。合并后的参数为：

$$
\theta_{\mathrm{merged}} = \sum_{i=1}^{n} \alpha_i \theta_i,
\quad \alpha_i \geq 0, \quad \sum_{i=1}^{n} \alpha_i = 1
$$

系数 $\{\alpha_i\}$ 在 held-out validation set 上优化，使合并模型损失最小。

## Validation Set Design

关键设计是 validation set 必须对所有训练子集都是 **OOD（out-of-distribution）**：使用各子集策略 rollout 收集的 DAgger 恢复轨迹。这些恢复行为天然不在原始训练数据中，因此能无偏地评估合并策略对未见过状态的泛化能力。

## Souping Strategies

常见权重选择/搜索策略包括：

- **Average weighting**：$\alpha_i = 1/n$，均匀平均。
- **Inverse-loss weighting**：$\alpha_i \propto 1 / (L_i + \epsilon)^p$，验证损失越低权重越高。
- **Gradient descent**：将 $\alpha$ softmax 参数化，迭代最小化合并模型在验证集上的损失。
- **Greedy search**：逐次加入能最大程度降低验证损失的检查点，并用均匀平均组合已选集合。

## Comparison with Alternatives

| 方法 | 机制 | 与 MA 的区别 |
|---|---|---|
| Mixture-of-Experts (MoE) | 训练时引入显式 router | MA 无需路由器和额外训练结构 |
| Deep Ensembles | 推理时聚合多个模型输出 | MA 直接合并参数，推理开销与单模型相同 |
| Joint Training | 把所有子集混在一起训练 | MA 通常优于 joint training，说明微调后的 VLA 存在参数冗余，分片训练能找到互补模式 |

## Pros & Cons

- **优点**：
  - 不增加推理成本；
  - 无需额外数据采集；
  - 能把多个“单模态”策略合成“多模态”统一策略。
- **局限**：
  - 要求子集策略在相同架构/初始化下训练；
  - 验证集质量决定合并效果；
  - 目前主要在相同任务的数据子集上验证，跨任务合并仍是开放问题。

## Related Concepts

- [[Distributional-Inconsistencies-in-Robot-Learning]] — MA 所针对的分布不一致框架
- [[Train-Deploy-Alignment]] — χ0 中另一对齐模块
- [[Stage-Advantage]] — χ0 中另一对齐模块
- [[Imitation-Learning]] — MA 改善的模仿学习范式
- [[Mixture-of-Experts]] — 另一种多策略组合思路

## Papers

- [[05_Papers/articles/chi0|χ0: Resource-Aware Robust Manipulation via Taming Distributional Inconsistencies]]
- Wortsman et al., "Model soups: Averaging weights of multiple fine-tuned models improves accuracy without increasing inference time", ICML 2022
