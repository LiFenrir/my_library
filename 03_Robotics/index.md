---
title: "03_Robotics"
description: "机器人底层技术知识库：感知、规划、控制、硬件、ROS2、机器人工程。"
tags: [moc, robotics, perception, planning, control]
created: 2026-07-22
---

# 03_Robotics

机器人系统底层技术：感知、规划、控制、硬件、中间件与工程实践。

具身智能的算法与模型（VLA、World Model、机器人 RL）请移步 [[04_Embodied-AI/index|04_Embodied-AI]]。

## 子领域

- [[03_Robotics/Perception/index|Perception]] — 视觉、点云、状态估计、SLAM、坐标系、标定
  - [[03_Robotics/Perception/Coordinate-Frames|Coordinate-Frames]] — 常见坐标系约定与转换速查
  - [[03_Robotics/Perception/URDF-Rendering-Calibration|URDF-Rendering-Calibration]] — URDF 渲染与真实画面几何对齐
- [[03_Robotics/Planning/index|Planning]] — 运动规划、任务规划、决策
  - [[03_Robotics/Planning/Model-Predictive-Control|Model-Predictive Control]] — 基于前向模型的滚动时域优化控制
- [[03_Robotics/Control/index|Control]] — 控制理论、力控、阻抗控制
  - [[03_Robotics/Control/Outer-Loop-Guidance|Outer-Loop Guidance]] — VLA 作为控制外环的分层架构
  - [[03_Robotics/Control/Inverse-Dynamics|Inverse Dynamics]] — 逆动力学
  - [[03_Robotics/Control/Robot-Action-Space|Robot Action Space]] — 机器人动作空间
  - [[03_Robotics/Control/Robot-Observation-Space|Robot Observation Space]] — 机器人观测空间
- [[03_Robotics/Simulation/index|Simulation]] — 仿真、Real2Sim、评估基准
  - [[03_Robotics/Simulation/Real2Sim-Pipeline|Real2Sim-Pipeline]] — 真实场景转仿真资产
  - [[03_Robotics/Simulation/Disentangled-Robot-Generalization-Benchmark|Disentangled Generalization Benchmark]] — 解耦泛化评估
- Hardware — 机械臂、末端执行器、传感器、嵌入式（待填充）
- ROS2 — ROS2 中间件、通信、工具链（待填充）
- [[03_Robotics/Robot-SDK/index|Robot SDK]] — 机器人 SDK、接口、仿真平台（待填充）

## 概念与方法

- [[03_Robotics/Fundamentals/Dynamics-Model|Dynamics-Model]] — 机器人动力学模型

## 与相关目录的关系

- [[04_Embodied-AI/index|04_Embodied-AI]] — 具身智能算法与模型
- [[05_Papers/index|05_Papers]] — 论文精读
- [[06_Projects/index|06_Projects]] — 机器人项目实践

## 概念链

```
Concept → Theory → Paper → Engineering → Experiment → Project
```
