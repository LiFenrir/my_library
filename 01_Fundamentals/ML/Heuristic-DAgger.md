---
title: Heuristic DAgger
description: 通过将机器人初始化到人工设计的失败状态来离线采集恢复演示的 DAgger 变体
tags:
  - fundamentals
  - ml
  - imitation-learning
  - dagger
  - concept
created: 2026-07-30
---

# Heuristic DAgger

Heuristic DAgger 是 [[DAgger|Dataset Aggregation]] 的一种变体。它不再等待策略在真实 rollout 中自然失败，而是 **把系统直接初始化到人工设计的失败状态**，由专家采集恢复轨迹，从而高效地把恢复行为注入训练数据。

## Why

标准 DAgger 的流程是：

1. 用当前策略在真实环境中执行；
2. 等待策略进入错误/失败状态；
3. 专家接管并提供纠正动作；
4. 将纠正轨迹加入数据集重新训练。

问题在于：

- 自然失败出现得慢且不可控；
- 某些高风险失败状态难以通过策略自然到达；
- 数据采集周期长、机器人利用率低。

## Core Idea

把步骤 1-2 反过来：先定义好代表性失败状态（如错位抓取、部分掉落、遮挡、织物缠绕），再直接把机器人置于此状态，然后采集专家恢复演示。

形式化上，它同样扩展 $P_{\mathrm{train}}$ 到失败相邻区域，实现 DAgger 的分布对齐目标，但把 **online failure discovery** 替换为 **offline heuristic initialization**。

## Typical Failure States

在机器人操作中，常设计的失败状态包括：

- 抓取点偏移或打滑；
- 物体部分掉落、折叠或缠绕；
- 双臂协调失败导致目标姿态偏离；
- 长程任务中某一阶段未完成就进入下一阶段。

## Pros & Cons

- **优点**：
  - 大幅缩短恢复数据采集时间；
  - 可覆盖策略自然 rollout 难以触达的危险失败状态；
  - 无需复杂的在线人机交互系统。
- **局限**：
  - 失败状态设计依赖任务先验；
  - 人工初始状态可能无法完全复现真实部署中的失败分布；
  - 恢复演示质量直接决定策略改进上限。

## Relationship to Standard DAgger

| | Standard DAgger | Heuristic DAgger |
|---|---|---|
| 失败来源 | 策略自然 rollout | 人工设计初始化 |
| 在线/离线 | 在线 | 离线 |
| 覆盖范围 | 受策略探索能力限制 | 受设计空间限制 |
| 时间成本 | 高 | 低 |
| 对专家依赖 | 实时纠正 | 预定义状态 + 纠正 |

## Related Concepts

- [[Imitation-Learning]] — Heuristic DAgger 所属范式
- [[Human-Gated-DAgger]] — 另一种在线专家介入变体
- [[Train-Deploy-Alignment]] — Heuristic DAgger 在 χ0 中的应用框架
- [[Distributional-Inconsistencies-in-Robot-Learning]] — 失败恢复数据的分布对齐目标

## Papers

- [[05_Papers/articles/chi0|χ0: Resource-Aware Robust Manipulation via Taming Distributional Inconsistencies]]
- Ross et al., "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning", AISTATS 2011
