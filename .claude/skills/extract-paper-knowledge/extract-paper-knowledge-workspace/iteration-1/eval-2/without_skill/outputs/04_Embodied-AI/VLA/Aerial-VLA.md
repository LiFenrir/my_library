---
title: "Aerial VLA"
description: "面向无人机的视觉-语言-动作模型：语言驱动的空中自主与边缘推理。"
tags: [vla, aerial-robot, uav, embodied-ai]
created: 2026-07-28
---

# Aerial VLA

将 VLA 应用于空中机器人（UAV）时，需要同时满足快速反应与高层语义理解：前者用于外环制导，后者用于障碍物描述、跑道感知和向操作员汇报。

## 核心挑战

- 空中平台视觉变化快，反应延迟直接影响安全。
- 机载算力严格受限（如 Jetson AGX Orin）。
- 动作 token 应作为外环制导指令（速度、航向、航点），而非直接电机指令。

## 相关系统

- SINGER、VLA-AN、AerialVLA、AIR-VLA、AirVLA、LiteVLA-H

## 设计原则

- 快慢分离：快分支做外环制导，慢分支做语义感知。
- 保留传统飞控内环稳定，VLA 不替代底层控制器。
- 语义输出作为监督信号，不作为硬实时控制信号。

## 来源

- LiteVLA-H: 第 1-2 节、第 9 节
