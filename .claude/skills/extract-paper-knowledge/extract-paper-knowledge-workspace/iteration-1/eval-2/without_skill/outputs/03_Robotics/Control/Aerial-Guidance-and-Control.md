---
title: "Aerial Guidance and Control"
description: "空中机器人的外环制导与内环稳定分层控制，VLA 作用于外环而非直接驱动电机。"
tags: [aerial-robot, control, guidance, uav]
created: 2026-07-28
---

# Aerial Guidance and Control

空中机器人通常采用分层控制：外环负责高层制导决策，内环负责高频姿态稳定。VLA 等语义感知模块应置于外环，而非替代底层飞控。

## 分层结构

- **外环 (Outer-loop)**: 生成速度、航向、航点或模式级指令；更新率较低（如 20 Hz）。
- **内环 (Inner-loop)**: 姿态、角速度、电机控制；更新率高，保证平台稳定。

## VLA 的定位

- VLA 输出短视界动作 token，作为外环制导输入。
- 下游控制器负责命令验证、包络限幅、紧急停止等安全逻辑。
- 语义输出仅作监督和操作员支持，不作为硬实时控制信号。

## 安全实践

- 拒绝过期动作 token。
- 将命令限制在车辆特定包络内。
- 低置信度或危险触发时回退到悬停、刹车、返航或经典避障。

## 来源

- LiteVLA-H: 第 3.1 节、第 9.2 节
