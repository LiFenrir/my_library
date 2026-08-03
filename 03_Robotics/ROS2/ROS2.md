---
title: "ROS2"
description: "机器人操作系统第二版，用于机器人软件模块化通信与部署"
tags: [concept, robotics, ros2, middleware]
created: 2026-07-30
---

# ROS2

**核心定义**：ROS2（Robot Operating System 2）是用于机器人软件开发的中间件框架，提供节点间通信、参数管理、 launch 系统、实时支持等功能，是机器人系统集成与部署的事实标准之一。

## 核心特性

- **DDS 中间件**：基于 Data Distribution Service，支持去中心化、QoS 策略；
- **多机器人支持**：原生支持分布式多机器人系统；
- **实时性**：比 ROS1 更好的实时控制支持；
- **跨平台**：支持 Linux、Windows、macOS 及嵌入式系统。

## 常用概念

- Node、Topic、Service、Action
- Launch 文件
- Parameter Server
- RViz / Gazebo 集成

## 在 VLA 中的应用

- 将 VLA 推理节点与底层控制节点解耦；
- 通过 Topic 接收图像和本体感知；
- 通过 Action/Topic 发布动作命令。

## 与其他概念的关系

- [[04_Embodied-AI/VLA/VLA-ROS2-Integration|VLA ROS2 Integration]] — VLA 与 ROS2 的系统集成
- [[03_Robotics/Control/Robot-Action-Space|Robot Action Space]] — ROS2 中发布的控制目标

## 来源

- 通用机器人工程概念
