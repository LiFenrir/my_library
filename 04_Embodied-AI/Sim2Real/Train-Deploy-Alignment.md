---
title: Train-Deploy Alignment
description: 通过数据增广、启发式 DAgger 和动作块平滑桥接机器人训练分布与部署分布
tags:
  - embodied-ai
  - sim2real
  - robot-learning
  - deployment
  - concept
created: 2026-07-30
---

# Train-Deploy Alignment

Train-Deploy Alignment（TDA）是一套把机器人训练分布 $P_{\mathrm{train}}$ 向真实部署分布 $P_{\mathrm{test}}$ 对齐的策略组合，重点解决 inference-control latency、执行漂移和失败恢复问题。

## Why

即使策略在训练分布上表现良好，真实部署时仍会遇到两类不一致：

1. **推理-执行延迟**：模型输出动作到电机实际执行之间存在延迟，导致动作块之间衔接不连续、漂移累积；
2. **失败级联**：训练数据通常只包含成功轨迹，缺乏从失败状态恢复的行为，一旦部署中出现扰动策略无法自愈。

## Core Components

TDA 包含三个互补模块：

### 1. Heuristic DAgger

标准 DAgger 需要让策略 rollout 到自然失败再由专家纠正，耗时且不可控。Heuristic DAgger 直接 **把系统初始化到人工设计的失败状态**（如错位抓取、部分掉落），然后采集恢复演示。

- 把恢复行为前置到数据收集阶段；
- 无需等待策略自然失败，数据收集更高效；
- 与标准 DAgger 同样能扩展 $P_{\mathrm{train}}$ 到失败相邻区域。

### 2. Spatio-Temporal Augmentation

在零机器人时间的情况下多样化 $P_{\mathrm{train}}$：

- **水平翻转 + 左右臂交换**：利用双臂任务的对称性；
- **部分帧跳过（frame-skipping）**：合成速度变化，增强对执行节奏的鲁棒性。

### 3. Temporal Chunk-wise Smoothing

处理 action-chunking 策略在部署时的延迟与块间不连续：在旧动作缓冲区与新预测块之间做重叠区域的线性插值，平滑过渡。

数学上维护当前缓冲区 $\mathbf{a}^{\mathrm{old}}$、消费索引 $k$、新块 $\mathbf{a}^{\mathrm{new}}$，以及最大丢弃长度 $d_{\mathrm{max}}$ 和最小重叠长度 $m_{\mathrm{min}}$，按 [[Temporal-Chunk-wise-Smoothing|Temporal Chunk-wise Smoothing]] 算法更新输出缓冲区。

## Interaction with Action Chunking

TDA 与 RTC（[[Real-time-Action-Chunking]]）等方法正交：

- RTC 在 **训练时** 模拟延迟，使模型学会生成延迟兼容的动作；
- Temporal chunk-wise smoothing 在 **部署时** 平滑新旧动作块交接，可直接叠加在 RTC 上进一步降低漂移。

## Pros & Cons

- **优点**：
  - 同时覆盖数据层面（DAgger、增广）和执行层面（平滑）的对齐；
  - Heuristic DAgger 显著降低恢复数据采集成本；
  - 平滑策略提高控制吞吐和动作连续性。
- **局限**：
  - Heuristic DAgger 的失败状态设计依赖任务知识；
  - 帧跳过等增广只在特定任务有效；
  - DAgger 数据会提高重试成本，属于成功率与运行成本的 trade-off。

## Related Concepts

- [[Temporal-Chunk-wise-Smoothing]] — TDA 的执行平滑算法
- [[Heuristic-DAgger]] — TDA 的数据收集变体
- [[Distributional-Inconsistencies-in-Robot-Learning]] — TDA 在 χ0 中的定位
- [[Action-Chunking]] / [[Real-time-Action-Chunking]] — 相关动作块技术
- [[Human-Gated-DAgger]] — 另一种专家介入的数据收集方式

## Papers

- [[05_Papers/articles/chi0|χ0: Resource-Aware Robust Manipulation via Taming Distributional Inconsistencies]]
