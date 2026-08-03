---
title: "Time-to-Success Evaluation"
description: "基于 time-to-success CDF 的 VLA 分布级评估方法论，替代传统二元成功率"
tags: [concept, embodied-ai, vla, evaluation, benchmarking, methodology]
created: 2026-08-03
---

# Time-to-Success Evaluation

将 VLA 评估从二元成功率升级为 time-to-success CDF 的分布级方法论，提供更丰富的性能区分度和统计可靠性。

## 核心原语

每次 robot rollout 建模为随机变量 $T$（首次成功放置的墙钟时间）：

- **成功**: 记录实际完成时间
- **不可恢复失败**（物品掉出工作区、安全停机）: $T = \infty$，视为 ghost event
- **超时**: 右截尾（recoverable slow tail），不视为失败

CDF 使用 Kaplan-Meier 估计，置信区间用 episode 聚类 bootstrap。

## HRT 评分

Human-Relative Throughput — 以同装置人类遥操作速度为参考的无量纲比率：

$$\mathrm{HRT}(m, o) = \frac{\mathrm{RMST}_{\text{Human}, o}(\tau)}{\mathrm{RMST}_{m, o}(\tau)}, \quad \tau = 240s$$

- 综合速度与完成率（硬失败通过 $T = \infty$ 抬高模型 RMST）
- HRT 用于排名，KS 检验用于判断排名是否统计显著

## 关键洞察

1. **不同标量可给出相反排序**: RMST/HRT 排名 ≠ AUC 排名，headline scalar 是一种方法论承诺
2. **分布级检验比标量检验功效高**: KS 检验在 N≤30/cell 可比二元检验提升 30 倍样本效率
3. **空间配置是关键混淆因素**: 相机位置可造成 22pp 完成率波动，盲法同场轮换至关重要
4. **硬失败应拆机制分析**: 相同硬失败率可能对应完全不同的失效模式（掉落 vs 安全停机 vs 超时）

## 协议要素

- 盲法随机调度（操作员不知当前运行哪个模型）
- 同场同装置对比（消除 embodiment 和场景因素）
- 公开 rollout 视频供逐条审计
- 理论功效分析预先确定所需样本量

## 相关概念

- [[01_Fundamentals/ML/Kaplan-Meier-Estimator|Kaplan-Meier Estimator]]
- [[01_Fundamentals/ML/Kolmogorov-Smirnov-Test|Kolmogorov-Smirnov Test]]
- [[04_Embodied-AI/VLA/real-robot-vla-evaluation|Real-Robot VLA Evaluation]]

## 来源

- [[05_Papers/notes/phail|PhAIL]] — 分布级评估方法论的系统提出与验证
