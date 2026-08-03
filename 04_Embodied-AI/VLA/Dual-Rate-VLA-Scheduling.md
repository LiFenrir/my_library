---
title: Dual-Rate VLA Scheduling
description: 在单个 VLA 上同时支持高速动作引导与低速语义感知的双速率调度策略
tags:
  - embodied-ai
  - vla
  - scheduling
  - edge-inference
  - aerial-robotics
created: 2026-07-28
---

# Dual-Rate VLA Scheduling

Dual-Rate Scheduling 让同一个 compact VLA backbone 在边缘设备上同时服务两个时间尺度：

- **Fast action branch**：短 action token 输出，用于外环引导（如 ~20 Hz）。
- **Slow semantic branch**：句子级语义输出，用于场景理解、危险描述、操作员提示（如 ~6–7 Hz）。

## 核心观察

在 compact edge VLA 中，端到端延迟是 **pre-fill dominant** 的：生成第一个 action token 之前，绝大部分时间已经消耗在多模态 pre-fill 上。因此，额外解码几个语义 token 的边际成本很低，但语义生成不应阻塞动作分支的硬截止时间。

## 调度形式化

设动作查询周期为 Δ_a，语义查询周期为 Δ_s：

```
Δ_s = K · Δ_a,  K ∈ N, K > 1
```

当检测到危险谓词、置信度下降或任务状态转换时，可触发事件驱动的语义刷新。

## 截止时间优先策略

- **Action 查询**：立即准入，不得延迟。
- **Semantic 查询**：机会式、非阻塞；在动作 deadline 空闲时执行。

示例：K=3 时，三个动作周期约为 151.95 ms，与单句语义延迟 149.90 ms 接近，因此可以每第三次动作周期刷新一次语义。

## 与单速率系统的对比

| 方案 | 动作频率 | 语义频率 | 问题 |
|------|----------|----------|------|
| 单速率语义 | 被拖累至 ~6.67 Hz | ~6.67 Hz | 浪费模型的快速首 token 能力 |
| Dual-rate | ~19.74 Hz | ~6.67 Hz | 保持动作 deadline，同时保留语义通道 |

## 工程含义

- 动作与语义输出应被视为不同优先级的服务，而非可互换的请求。
- 内存/功耗开销通常很小（例如额外 0.1 GB 内存、3.6 W 功耗）。
- 预测、记忆等模块（如 FutureVLA、ReMem-VLA 风格）应选择性激活，避免在需要快速反应时增加 TTFA。

## 补充：来自 [[04_Embodied-AI/VLA/Dual-Rate-VLA-Scheduling|dual-rate-vla-scheduling（已合并）]]

总延迟可分解为：

$$
L(n) = P(I_t, x_t, m_t) + \sum_{i=1}^{n} D_i
$$

- $P(\cdot)$：多模态预填充（pre-fill）成本；$D_i$：解码第 $i$ 个 token 的成本。
- 在边缘设备上，对于短输出通常满足 $P \gg D_i$，即系统处于 pre-fill 主导状态。因此减少输出 token 数量对延迟改善有限，保护首次 token 的截止时间比统一调度更重要。

优缺点补充：

- **优点**：一个共享 backbone 同时满足实时控制和语义感知；内存和功耗开销小。
- **局限**：语义信息不是每帧都有；需要仔细的调度策略避免动作 deadline miss；仅在 pre-fill 主导场景收益明显。

## Related Concepts

- [[Edge-VLA-Inference|Edge VLA Inference]] — pre-fill dominant 的延迟特征是 dual-rate 调度的基础
- [[Outer-Loop-Guidance|Outer-Loop Guidance]] — 快速动作分支的输出层级与安全边界
- [[Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — 让同一模型同时保留动作与语义能力
- [[Aerial-VLA|Aerial VLA]] — 无人机等 aerial 平台对双速率调度的典型需求

## Papers

- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 本笔记主要知识来源
