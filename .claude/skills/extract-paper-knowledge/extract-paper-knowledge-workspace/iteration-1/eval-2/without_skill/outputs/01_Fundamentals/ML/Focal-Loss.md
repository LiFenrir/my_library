---
title: "Focal Loss"
description: "通过降低易分样本权重来缓解类别不平衡的损失函数，常用于目标检测与稀少正样本任务。"
tags: [ml, loss-function, classification, imbalance]
created: 2026-07-28
---

# Focal Loss

Focal Loss 通过引入调制因子 $(1 - p_t)^\gamma$ 降低易分样本的损失权重，使模型更关注难分样本，缓解极端类别不平衡。

## 公式

$$
FL(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)
$$

其中 $p_t$ 是模型对真实类别的预测概率，$\alpha_t$ 平衡正负样本，$\gamma$ 控制难易样本权重。

## 机器人应用

- ARM 用 Focal Loss 训练任务完成头：长程连续轨迹中成功终止帧极其稀少，正样本严重稀缺。
- 参数示例：$\gamma = 2.0$，$\alpha = 2.0$。

## 来源

- ARM: 第 3.2.1 节、附录 Table 6
- Lin et al., 2018
