---
title: Aerial VLA
description: 面向无人机等空中平台的 Vision-Language-Action 模型：兼顾快速反应与高层语义理解
tags:
  - embodied-ai
  - vla
  - aerial-robotics
  - robotics
  - edge-inference
created: 2026-07-28
---

# Aerial VLA

Aerial VLA 将 Vision-Language-Action 模型应用于无人机（UAV）等空中平台，使其能够根据视觉观测和语言指令进行导航、避障、着陆与任务执行，同时保留对场景的语义解释能力。

## 与操作 VLA 的区别

空中机器人对 VLA 提出了更严格的时序要求：

- **视觉变化快**：高度、速度、视角变化迅速，需要低延迟反应。
- **平台动态不稳定**：不能等待长句子生成后再更新轨迹。
- **机载算力受限**：通常依赖 Jetson 等边缘设备，必须 compact 模型。
- **通信受限**：部分任务需要完全 onboard 推理，不能依赖云端。

## 典型能力

- **低层导航**：起飞、降落、航点跟踪、避障。
- **高层语义**：障碍物描述、跑道/着陆区识别、场景摘要、危险告警。
- **人机协作**：向操作员解释当前状态与决策。

## 设计要点

1. **外环引导 + 内环稳定**：VLA 输出高层动作指令，飞控负责姿态稳定。
2. **双速率调度**：快速 action 分支与慢速 semantic 分支分离。
3. **边缘推理优化**：针对 pre-fill dominant 的延迟特征优化 TTFA。
4. **知识保持 fine-tune**：避免专业化后丢失通用视觉-语言能力。

## 安全边界

- 动作 token 应解释为速度/航向/航点/模式指令，而非直接电机控制。
- 设置指令包络、过期拒绝、置信度监控与紧急回退（悬停、返航）。

## Related Concepts

- [[Outer-Loop-Guidance|Outer-Loop Guidance]] — 分层控制架构
- [[Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 动作与语义双速率运行
- [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘推理延迟特征
- [[Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — 专业化时保留语义能力
- [[03_Robotics/Control/index|Control]] — 底层控制

## Papers

- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 本笔记主要知识来源
- 相关方向：SINGER、VLA-AN、AerialVLA、AIR-VLA、AirVLA
