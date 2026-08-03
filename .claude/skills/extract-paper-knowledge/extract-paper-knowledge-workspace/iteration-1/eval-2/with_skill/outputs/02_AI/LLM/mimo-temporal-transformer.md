---
title: "多输入多输出时序 Transformer"
description: "以 MIMO 方式在因果窗口内同时预测多个时步输出，用于相对优势估计等序列任务。"
tags: [concept, ai, transformer, sequence-modeling, robotics]
created: 2026-07-28
---

# 多输入多输出时序 Transformer

核心定义：在单个前向传播中同时接收多个历史观测并输出多个预测，避免传统滑动窗口的冗余计算。

## 原理

- 输入：因果窗口 $\mathcal{W}_t = \{o_{t-4k}, \dots, o_t\}$，包含视觉特征、本体感受状态与语言指令。
- 多模态融合：将三类输入投影到同一隐空间后相加或拼接。
- 输出：
  - 区间优势分类头：预测相邻状态间的相对进展（进步/退步/停滞）。
  - 任务完成头：预测当前状态是否为成功终止状态。

## MIMO vs MISO

- **MISO（Multi-Input Single-Output）**：每个前向只输出一个标量，冗余大。
- **MIMO**：一次前向输出多个时步预测，利用共享特征摊销计算。

## 来源

- [[05_Papers/articles/arm|ARM]] — ARM 的奖励模型采用 MIMO Temporal Transformer。
