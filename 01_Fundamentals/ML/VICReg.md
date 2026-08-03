---
title: VICReg
description: 通过方差、不变性与协方差正则化实现非样本对比自监督学习
tags:
  - concept
  - ml
  - self-supervised-learning
  - non-contrastive-learning
  - representation-learning
  - jepa
created: 2026-07-30
---

# VICReg

VICReg（Variance-Invariance-Covariance Regularization）是一种非样本对比的自监督学习方法。它不依赖负样本，而是通过正则化表示的统计特性来防止崩塌。

## 核心思想

给定输入 $x$ 与其变换/视角 $y$，分别编码为 $s_x$ 和 $s_y$。训练目标由三部分组成：

1. **方差（Variance）**：防止表示各分量崩塌为常数。
2. **不变性（Invariance）**：让同一内容的不同视图在表示空间中接近。
3. **协方差（Covariance）**：让表示不同分量尽可能去相关，最大化信息量。

## 实现要点

- 先将 $s_x$ 和 $s_y$ 通过可训练的 expander 映射到更高维嵌入 $v_x$、$v_y$。
- 方差损失：对每个分量维持标准差高于阈值（hinge 损失）。
- 协方差损失：将 $v$ 的协方差矩阵推向单位矩阵，使分量去相关。
- 不变性损失：$D(s_y, \tilde{s}_y)$，最简单情形令预测器为恒等映射，即 $\|s_y - s_x\|^2$。

## 与 JEPA 的关系

VICReg 可用于训练 [[Joint-Embedding-Predictive-Architecture|JEPA]]：

- 方差 + 协方差损失对应“最大化 $s_x$ 与 $s_y$ 信息量”。
- 不变性/预测损失对应“使 $s_y$ 易从 $s_x$ 预测”。
- 若预测器含隐变量 $z$，还需额外正则化 $z$ 的信息量。

## 对比方法 vs VICReg

| 维度 | 对比方法 | VICReg |
|------|----------|--------|
| 负样本 | 需要 | 不需要 |
| 对比对象 | 样本之间 | 表示分量之间 |
| 高维问题 | 负样本数可能指数增长 | 不受样本数限制 |

## 与其他概念的关系

- [[Self-Supervised-Learning|SSL]] — VICReg 是 SSL 的非对比实现。
- [[Joint-Embedding-Predictive-Architecture|JEPA]] — VICReg 可作为 JEPA 的训练准则。
- [[Energy-Based-Model|EBM]] — VICReg 通过正则化低能量区域体积训练 EBM。

## 来源

- Bardes et al., 2021
- [[05_Papers/articles/path-towards-autonomous-machine-intelligence|A Path Towards Autonomous Machine Intelligence]]，LeCun，2022
