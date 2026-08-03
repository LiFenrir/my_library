---
title: "PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology"
description: "提出以 time-to-success CDF 为评估原语，用 HRT 评分、KS 检验显著性，在 Franka FR3 上开放评估四个 VLA。"
tags: ["VLA", "Real-Robot", "Benchmark", "Evaluation-Methodology", "PhAIL", "HRT", "Kolmogorov-Smirnov", "Time-to-Success", "Franka-FR3"]
created: 2026-07-22
---

# PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology

## 基本信息

- **作者**: Sergey Arkhangelskiy (Positronic Robotics)
- **链接**: [arXiv:2605.29710](https://arxiv.org/abs/2605.29710), 项目站 <https://phail.ai>
- **发表**: arXiv preprint, 2026
- **原文**: [[05_Papers/articles/phail|phail.md|phail.md]]
- **PDF**: [[99_Attachments/papers/pdfs/phail.pdf|phail.pdf]]

## 研究背景

真实机器人 VLA 评估的通行做法是：固定超时下的二元成功率，N ≤ 25 rollouts/条件，无置信区间、无配对检验。样本量不足以区分性能接近的策略，且不同标量（UPH、完成率、cycle time）可能给出相反排序。方法学批评呼吁盲法同场 A/B 与数百次 rollout，但缺少可共享的评估原语和参考实现。

## 核心方法

### 1. time-to-success CDF 作为评估原语

- 每次操作视为随机变量 T（首次成功放置的墙钟时间）。
- **不可恢复失败**（物品掉出工作区、安全停机、episode 结束仍未捡起）吸收为 **T = ∞ 的 ghost event**。
- **超时**属于右截尾（recoverable slow tail），不是 ghost event。
- CDF 用 Kaplan–Meier 估计；置信区间用 episode 聚类 bootstrap。

### 2. 评分层：Human-Relative Throughput (HRT)

$$
\mathrm{HRT}(m, o) = \frac{\mathrm{RMST}_{\text{Human}, o}(\tau)}{\mathrm{RMST}_{m, o}(\tau)}, \quad \tau = 240\ \mathrm{s}
$$

- 以同装置人类遥操作作为参考，得到无量纲比率。
- 宏观平均四个物体（木勺、毛巾、剪刀、电池）。
- HRT 综合速度与完成率：硬失败通过 T = ∞ 抬高模型 RMST。

### 3. 显著性层：macro-averaged KS 检验

- 对每个 (model, object) cell 计算两样本 Kolmogorov–Smirnov 距离。
- 对四个物体等权宏观平均。
- 用 pooled-resample episode 聚类 bootstrap 计算 p 值，校准于 H0 而非依赖渐近 Kolmogorov 分布。
- **评分与显著性分离**：HRT 用于排名，KS 用于判断分布是否可区分。

## 实验设置

- **平台**: Franka Research 3 + Robotiq 2F-85 + 肩外/腕部 RGB 相机，DROID 式配置。
- **任务**: bin-to-bin 拣选四个训练物体（木勺、毛巾、剪刀、电池）。
- **数据**: ~995  episodes，其中 396 为同装置人类遥操作参考。
- **模型**: OpenPI π₀.₅、NVIDIA GR00T N1.6、ACT、SmolVLA，均在同一 449-episode 演示集上用各仓库默认 recipe fine-tune。
- **协议**: 每 rollout 30 s/item 上限；操作员盲法随机调度；仅安全停机可干预。

## 主要结果

| Model | RMST (s) [95% CI] | HRT (%) [95% CI] | Intervention rate | Episodes |
|---|---|---|---|---|
| Human reference (teleop) | 10.5 [10.3, 10.8] | 100.0 | — | 396 |
| OpenPI π₀.₅ | 77.7 [69.2, 87.0] | 13.8 [12.2, 15.7] | 4.2% | 165 |
| GR00T N1.6 | 77.2 [69.0, 86.4] | 13.3 [12.0, 15.2] | 4.2% | 165 |
| ACT | 100.9 [85.8, 117.6] | 10.5 [9.2, 13.2] | 2.0% | 151 |
| SmolVLA | 165.8 [147.0, 185.6] | 6.4 [5.7, 7.5] | 18.6% | 118 |

- **最佳 VLA 仍比人类慢约 7 倍**。
- **OpenPI 与 GR00T 统计不可区分**（HRT CIs 高度重叠，KS p = 0.12，logrank p = 0.54）。
- **ACT 明显弱于 OpenPI/GR00T**；**SmolVLA 最差**。
- KS 在 N ≤ 30/cell 即可分辨 GR00T vs ACT（N=25）和 OpenPI vs ACT（N=30），而二元 McNemar 基线需要 600–1500 配对 rollouts/cell，相差约 30 倍。
- 最接近 pair OpenPI vs GR00T 在 N=30 仍未解决，预测需 N≈45/cell 达到 80% 功效。

## 关键洞察

1. **同一 CDF 的不同标量可给出相反排序**：按 RMST/HRT，OpenPI > GR00T > ACT；按对人类参考的 AUC，ACT 反而领先。因此 headline scalar 是一种方法论承诺，应明确披露。
2. **测试选择比样本量更决定功效**：KS 作为分布级检验，对任意 F_a ≠ F_b 一致；基于单一标量的检验会漏掉大量 CDF 差异。
3. **空间配置是主要混淆因素**：同侧/对侧相机-tote 配置可使 GR00T 完成率波动 22 pp，盲法同场随机轮换至关重要。
4. **硬失败应拆机制看**：CDF 渐近线由「掉出工作区」「安全停机」「超时截尾」共同构成，相同硬失败率可能对应完全不同的失效模式。

## 可复现性与开放资产

- 所有 rollout 视频、遥测、事件标注公开，可用 run-explorer（基于 Rerun）逐条审计。
- 分析代码与论文源码：<https://github.com/Positronic-Robotics/phail-paper>
- 数据集与排行榜：<https://phail.ai>

## 局限与未来

- 单一 embodiment、单一 primitive（bin-to-bin pick-and-place），经验验证限于四个物体。
- N≈35/cell 仍低于二元指标所需样本量；排名是方法说明性的。
- 未来扩展：插入、小零件装配、打包、导航、关节物体操作。

## 相关论文

- [[pi0-7|π₀ / π₀.5 / π₀.6 系列]]
- [[characterizing-vla-models|Characterizing VLA Models]]
- [[litevla-edge|LiteVLA-Edge]]
- [[litevla-h|LiteVLA-H]]
- [[pirl|PIRL]]
- [[rl-token-bootstrapping|RL Token Bootstrapping]]
