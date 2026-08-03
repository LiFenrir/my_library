---
title: "Real-Time VLA Inference"
description: "VLA 在边缘设备上的延迟分解、预填充主导性与双速率调度策略。"
tags: [vla, inference, edge, latency, real-time]
created: 2026-07-28
---

# Real-Time VLA Inference

紧凑型 VLA 在边缘设备部署时，端到端延迟往往由多模态预填充（multimodal pre-fill）主导，而非解码额外 token 的边际成本。

## 关键概念

- **Time-to-First-Action (TTFA)**: 从模型查询到首个有效动作 token 的延迟，是反应式控制的真正瓶颈。
- **Pre-fill Dominance**: 在小输出长度下，$P \gg D_i$，即图像-文本融合阶段占总延迟绝大部分。
- **Dual-Rate Scheduling**: 同一模型以不同周期服务两个分支：快分支输出动作 token，慢分支输出语义描述。

## 典型数据

- LiteVLA-H 在 Jetson AGX Orin 上：动作分支 50.65 ms (19.74 Hz)，语义分支 149.90 ms (6.67 Hz)。
- 预填充占比 $\rho \approx 0.944$。

## 优化方向

- 减少视觉 token 数量
- 缓存可复用的 prompt 结构
- 简化 projector 计算
- 重叠图像预处理与当前控制执行

## 来源

- LiteVLA-H: 第 2-3 节、第 6 节
