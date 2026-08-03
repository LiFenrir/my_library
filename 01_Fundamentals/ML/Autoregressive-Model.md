---
title: "Autoregressive Model"
description: "逐 token 生成输出，将每个新元素条件于已生成序列的概率模型"
tags: [concept, fundamentals, ml, generative-model]
created: 2026-07-30
---

# Autoregressive Model

**核心定义**：自回归模型（Autoregressive Model）是一种按顺序生成数据的概率模型，每个新元素的生成都以之前已生成的所有元素为条件。

## 形式化

对于序列 $\mathbf{x} = (x_1, \dots, x_T)$，自回归模型将其联合分布分解为：

$$
p_\theta(\mathbf{x}) = \prod_{t=1}^{T} p_\theta(x_t \mid x_{<t})
$$

## 训练

通常使用 **Teacher Forcing**：在预测 $x_t$ 时，输入真实的 $x_{<t}$ 而非模型自身生成的历史。

## 应用

- 语言模型（GPT 系列）
- 音频生成
- 图像生成（如 PixelCNN）
- 机器人动作序列生成

## 优缺点

- **优点**：建模灵活、可处理变长序列、自然支持条件生成。
- **缺点**：生成必须串行，速度较慢；存在 Exposure Bias。

## 与其他概念的关系

- [[01_Fundamentals/ML/Teacher-Forcing|Teacher Forcing]] — 常用训练技巧
- [[01_Fundamentals/ML/Exposure-Bias|Exposure Bias]] — 训练-测试分布不一致问题

## 来源

- 通用机器学习概念
