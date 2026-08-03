---
title: "MIMO Temporal Transformer"
description: "多输入多输出的时序 Transformer，用于一次性预测多个帧间关系，提升推理效率。"
tags: [transformer, architecture, temporal-modeling, multimodal]
created: 2026-07-28
---

# MIMO Temporal Transformer

MIMO（Multi-Input Multi-Output）时序 Transformer 将奖励/优势估计从单输出回归扩展为序列到序列预测，使模型能够利用短期历史上下文一次性输出多个帧间关系。

## 与 MISO 的区别

- **MISO**: 多个输入压缩为单个标量输出，丢失帧间细节。
- **MIMO**: 保留时间维度，输出每个时间步的表示，支持并行的多帧优势预测。

## 设计要点

- 因果窗口：仅使用过去帧，兼容在线与离线 RL。
- 多模态融合：视觉、本体感受、语言指令映射到统一潜空间。
- 并行推理：非重叠视频片段可批量处理，避免滑动窗口冗余计算。

## 应用

- ARM 用 MIMO 在 5 输出配置下达到 14.1 it/s，较 SARM 提升 3.6 倍。

## 来源

- ARM: 第 3.2 节、第 4.4 节
