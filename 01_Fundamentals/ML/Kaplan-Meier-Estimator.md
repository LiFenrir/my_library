---
title: "Kaplan-Meier Estimator"
description: "非参数生存分析估计器，用于处理含截尾数据的概率估计，在机器人评估中用于 time-to-success 建模"
tags: [concept, ml, statistics, survival-analysis, evaluation]
created: 2026-08-03
---

# Kaplan-Meier Estimator

Kaplan-Meier (KM) 估计器是非参数统计方法，用于从不完整（含右截尾）观测数据中估计生存函数 $S(t) = P(T > t)$。

## 定义

$$\hat{S}(t) = \prod_{t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$$

- $t_i$: 观测到的事件时间点
- $d_i$: 在 $t_i$ 发生的失败（事件）数
- $n_i$: 在 $t_i$ 之前仍处于风险中的样本数

## 在机器人评估中的应用

将每次操作视为随机变量 $T$（首次成功的墙钟时间）：

- **观测到成功**: 完整观测，按实际时间计入
- **不可恢复失败**（物品掉落、安全停机）: 视为 $T = \infty$ 的 ghost event，CDF 渐近线低于 1
- **超时截尾**: 右截尾（right-censored），KM 处理为"在 $t_{\text{timeout}}$ 时仍存活"

优势：
- 无需所有 trial 都完成即可估计完整分布
- 截尾与失败在 CDF 上产生可区分信号
- 比二元成功率携带更丰富的时间效率信息

## 置信区间

用 episode 聚类 bootstrap 计算，保留每个 episode 内 trial 的相关性结构。

## 相关概念

- [[01_Fundamentals/ML/Kolmogorov-Smirnov-Test|Kolmogorov-Smirnov Test]] — 比较两个 CDF 的非参数检验
- [[04_Embodied-AI/VLA/Time-to-Success-Evaluation|Time-to-Success Evaluation]] — VLA 评估方法论

## 来源

- [[05_Papers/notes/phail|PhAIL]] — KM 估计器在真实机器人 VLA 评估中的系统应用
