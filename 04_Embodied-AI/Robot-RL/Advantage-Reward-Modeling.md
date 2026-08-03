---
title: Advantage Reward Modeling
description: 通过估计相对优势而非绝对进度，为长程机器人操作提供可扩展、任务无关的奖励信号
tags:
  - embodied-ai
  - robot-rl
  - reward-model
  - vla
  - arm
created: 2026-07-28
---

# Advantage Reward Modeling (ARM)

用相对优势（relative advantage）替代绝对进度（absolute progress）来建模长程机器人操作中的密集奖励信号。

## Why

长程操作任务中，稀疏奖励难以提供足够信用分配信号，而密集进度奖励存在以下瓶颈：

- 需要任务相关的启发式或人工子任务分段；
- 绝对进度假设进度随时间单调递增，无法刻画真实演示中的回退、重试、恢复等非单调行为；
- 零样本 VLM 标注存在空间几何 grounding 不足、推理成本高、信号抖动等问题。

ARM 的核心洞察：相对优势比绝对进度更直观、更简洁、更任务无关。

## Core Idea

将奖励估计从“当前完成了多少”转化为“最近这段轨迹相比历史状态是推进、停滞还是回退”。通过三态相对优势标签训练奖励模型，再用任务完成锚点重建全局连续进度曲线。

## How It Works

### 输入与架构

采用 **MIMO（Multi-Input Multi-Output）Temporal Transformer**，在因果窗口 $\mathcal{W}_t = \{ o_{t-4k}, \dots, o_t \}$ 内同时处理多帧观测：

- **CLIP 视觉特征** $v_i$；
- **机器人本体状态** $s_i$（关节位置、夹爪状态等）；
- **任务语言指令** $g$。

三者通过 MLP 投影到统一潜在空间后相加，再输入 8 层 Transformer Encoder 得到时序增强的隐状态 $h_i$。

与 MISO（Multi-Input Single-Output）不同，MIMO 在一个前向过程中输出多个相邻帧之间的优势预测，避免冗余计算并保留局部时序上下文。

### 双头学习目标

1. **Multi-frame Advantage Classification**：区间头预测相邻隐状态之间的优势转移 $\Delta \hat{y}$，使用三态标签监督，损失为交叉熵 $\mathcal{L}_{\text{int}}$。
2. **Task Completion Prediction**：完成头预测当前观测为成功终止状态的概率 $C_t$，用 [[Focal-Loss|Focal Loss]] 处理类别不平衡。

总目标：

$$
\mathcal{L}_{ARM} = \lambda_{\text{int}} \mathcal{L}_{\text{int}} + \lambda_{\text{succ}} \mathcal{L}_{\text{succ}}
$$

### 输出

- 局部相对优势（用于识别推进/回退/停滞）；
- 全局任务完成锚点（用于将离散优势积分成连续进度曲线）。

## 补充：来自 [[04_Embodied-AI/Robot-RL/Advantage-Reward-Modeling|advantage-reward-modeling（已合并）]]

### 三态标签定义

对于观测对 $(s_t, s_{t+k})$，相对优势标签 $y \in \{-1, 0, +1\}$：

- **+1 Progressive**：状态有效向目标推进
- **-1 Regressive**：状态偏离目标、遇到错误或失败
- **0 Stagnant**：没有实质性进展，如等待或空闲

### 全局进度重建流程

将离散的相对优势预测整合为全局密集进度曲线 $P_t$：

- 将长轨迹切分为非重叠片段，并行处理
- 用任务完成头提供的绝对锚点（$P_T = 1.0$）校准
- 通过累加 $\Delta \hat{y}$ 重建完整进度曲线

详见 [[05_Papers/articles/arm|ARM]] 第 3 节。

## Related Concepts

- [[Tri-state-Advantage-Labeling]] — 训练 ARM 的轻量标注策略
- [[Global-Progress-Reconstruction]] — 将 ARM 离散预测转化为密集全局进度曲线
- [[Advantage-Weighted-Behavior-Cloning]] — 使用 ARM 信号进行样本加权的策略优化
- [[Long-Horizon-Manipulation-Reward]] — 长程操作奖励设计的共性问题
- [[Focal-Loss]] — 完成头使用的类别不平衡损失
- [[Imitation-Learning]] / [[Offline-Reinforcement-Learning]] — 下游学习范式
- [[Vision-Language-Action]] — ARM 所服务的策略模型背景

## Papers

- [[arm]] — ARM: Advantage Reward Modeling for Long-Horizon Manipulation
