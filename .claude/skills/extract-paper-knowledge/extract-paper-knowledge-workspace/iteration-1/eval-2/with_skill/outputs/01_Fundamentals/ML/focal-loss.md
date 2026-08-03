---
title: "Focal Loss"
description: "通过降低易分样本权重来缓解类别不平衡的损失函数。"
tags: [concept, fundamentals, loss-function, class-imbalance]
created: 2026-07-28
---

# Focal Loss

核心定义：在交叉熵基础上加入调制因子，让模型更关注难分样本，缓解类别不平衡。

## 公式

原始形式：

$$
\mathrm{FL}(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)
$$

- $p_t$：模型对真实类别的预测概率。
- $\gamma$：聚焦参数，降低易分样本损失。
- $\alpha_t$：类别权重，处理类别比例失衡。

## 适用场景

- 长程任务中成功终止帧极其稀少。
- 目标检测、分割等前景/背景不平衡问题。

## 来源

- [[05_Papers/articles/arm|ARM]] — 用于任务完成头（completion head）训练。
