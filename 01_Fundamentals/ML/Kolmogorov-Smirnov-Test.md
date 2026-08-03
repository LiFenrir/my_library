---
title: "Kolmogorov-Smirnov Test"
description: "比较两个分布的非参数统计检验，用于判断两组样本是否来自同一分布"
tags: [concept, ml, statistics, hypothesis-testing, evaluation]
created: 2026-08-03
---

# Kolmogorov-Smirnov Test

Kolmogorov-Smirnov (KS) 检验是比较两个累积分布函数 (CDF) 的非参数统计方法，检验原假设 $H_0: F = G$（两组样本来自同一分布）。

## 检验统计量

两样本 KS 距离：

$$D_{n,m} = \sup_x |F_n(x) - G_m(x)|$$

$F_n$ 和 $G_m$ 分别为两组样本的经验 CDF。$D_{n,m}$ 取两 CDF 在任意点的最大垂直距离。

## 在 VLA 评估中的优势

与二元成功率检验（McNemar）对比：

- **分布级检验**: 对任意 $F_a \neq F_b$ 一致（omnibus），不局限于单一标量差异
- **统计功效高**: 在 $N \leq 30$/cell 即可分辨显著差异，二元检验需要 600–1500 配对 rollouts
- **评分与显著性分离**: HRT 用于排名，KS 用于判断排序的统计可靠性

## 实现要点

- 使用 pooled-resample episode 聚类 bootstrap 计算 p 值
- 校准于 $H_0$ 而非依赖渐近 Kolmogorov 分布（小样本下不准确）
- 多条件宏观平均：对各 cell 的 KS 距离等权平均

## 局限性

- 对 CDF 尾部分布差异不敏感（尾部样本少）
- 最接近的配对可能需要更大样本量才能达到 80% 统计功效

## 相关概念

- [[01_Fundamentals/ML/Kaplan-Meier-Estimator|Kaplan-Meier Estimator]] — CDF 估计的前置步骤

## 来源

- [[05_Papers/notes/phail|PhAIL]] — KS 检验在 VLA 性能比较中的系统验证
