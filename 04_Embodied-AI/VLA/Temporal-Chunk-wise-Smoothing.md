---
title: Temporal Chunk-wise Smoothing
description: 在动作块策略部署时通过重叠区插值平滑新旧动作块交接，降低推理-执行延迟导致的漂移
tags:
  - embodied-ai
  - robot-control
  - action-chunking
  - real-time
  - concept
created: 2026-07-30
---

# Temporal Chunk-wise Smoothing

Temporal Chunk-wise Smoothing 是一种用于 **action-chunking 机器人策略** 的部署时平滑算法。它通过在新旧动作块的重叠区域做线性插值，缓解 inference-control latency 导致的动作突变和漂移累积。

## Why

Action-chunking 策略一次预测未来 $H$ 步动作，但只在其中 $\hat{H}$ 步后重新查询模型。由于模型推理需要时间，新动作块生成时旧块往往还未执行完，简单切换会造成：

- 动作不连续、机械臂抖动；
- 块间漂移累积；
- 控制频率和稳定性下降。

## Core Idea

维护一个当前动作缓冲区 $\mathbf{a}^{\mathrm{old}}$ 和一个消费索引 $k$（表示已执行多少步）。当获得新预测块 $\mathbf{a}^{\mathrm{new}}$ 时，不是直接替换，而是：

1. 根据延迟丢弃新块前 $d = \min(k, d_{\mathrm{max}})$ 步已经“过期”的命令；
2. 保留旧缓冲的剩余命令，必要时用最后命令 padding 到最小重叠长度 $m_{\mathrm{min}}$；
3. 对重叠区 $L = \min(|\mathbf{a}^{\mathrm{old}}|, |\mathbf{a}_{\mathrm{rem}}^{\mathrm{new}}|)$ 做线性插值：

$$
w_i = 1 - \frac{i}{\max(L-1, 1)}, \quad
\tilde{a}_i = w_i a_i^{\mathrm{old}} + (1 - w_i) a_{\mathrm{rem},i}^{\mathrm{new}}
$$

4. 将插值结果与新块剩余后缀拼接为新的输出缓冲区，并重置 $k = 0$。

## Algorithm

输入：当前缓冲区 $\mathbf{a}^{\mathrm{old}}$、消费索引 $k$、新块 $\mathbf{a}^{\mathrm{new}}$、$d_{\mathrm{max}}$、$m_{\mathrm{min}}$
输出：更新后的缓冲区 $\mathbf{a}^{\mathrm{buf}}$、重置后的 $k$

```
reset k ← 0
d ← min(k, d_max)
if d ≥ |a_new|: return a_old, k

a_rem^new ← (a_d^new, ...)
if |a_old| < m_min: pad a_old by repeating last command
L ← min(|a_old|, |a_rem^new|)

for i = 0 to L-1:
    w_i ← 1 - i / max(L-1, 1)
    ã_i ← w_i * a_i^old + (1 - w_i) * a_rem,i^new

a_buf ← (ã_0, ..., ã_{L-1}) || (suffix of a_rem^new)
return a_buf, k
```

## Key Parameters

- **$d_{\mathrm{max}}$**：最大丢弃长度，限制因延迟丢弃的新块前缀步数；
- **$m_{\mathrm{min}}$**：最小重叠长度，保证插值有足够样本；
- **消费索引 $k$**：跟踪当前缓冲区内已执行动作的位置。

## Pros & Cons

- **优点**：
  - 实现简单，无需修改模型架构；
  - 不增加额外推理开销；
  - 可与 RTC 等训练时延迟模拟方法正交叠加。
- **局限**：
  - 假设动作空间适合线性插值；
  - 参数 $d_{\mathrm{max}}$、$m_{\mathrm{min}}$ 需要按任务和频率调参；
  - 对需要突然改变方向的接触任务可能过度平滑。

## Related Concepts

- [[Action-Chunking]] — 动作块策略基础
- [[Real-time-Action-Chunking]] — 训练时延迟模拟方法
- [[Train-Deploy-Alignment]] — TCS 所属的部署对齐框架
- [[Asynchronous-Inference-for-Robot-Control]] — 另一种隐藏推理延迟的策略

## Papers

- [[05_Papers/articles/chi0|χ0: Resource-Aware Robust Manipulation via Taming Distributional Inconsistencies]]
