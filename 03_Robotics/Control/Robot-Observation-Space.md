---
title: Robot Observation Space
description: 机器人策略输入的状态表示，通常包含多视角相机图像和本体感受信息
tags:
  - robotics
  - control
  - observation-space
  - robot-learning
created: 2026-07-28
---

# Robot Observation Space

Robot Observation Space 定义了机器人策略可获取的**环境状态表示**，通常包含视觉观察（相机图像）和本体感受（proprioception）两部分。

## Visual Observations

来自一个或多个相机的 RGB 图像：
- **Front camera**：场景全局视角
- **Wrist cameras**：手臂/夹爪附近的局部视角
- **Rear camera**（可选）：补充背面信息

多视角观察同时提供环境上下文和精细操作细节。

## Proprioception

机器人自身状态测量，常见包括：
- 关节位置 / 关节角度
- 关节速度
- 末端执行器位姿
- 夹爪开合状态

## History Observations

策略通常使用最近一段时间内的多帧观察作为输入，以捕捉动态信息和时序上下文。

## Tokenization

在 VLA 中，观察通常被编码为 token：
- 图像通过视觉编码器压缩为视觉 token
- 本体感受通过线性投影映射为 token

## Related Concepts

- [[03_Robotics/Control/Robot-Action-Space|Robot Action Space]] — 策略输出的控制信号
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — 处理多模态观察输入的模型
- [[04_Embodied-AI/VLA/Action-Chunking|Action Chunking]] — 基于历史观察预测未来动作

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 使用最多 4 个相机视角和 6 帧历史观察，以及关节状态作为输入
