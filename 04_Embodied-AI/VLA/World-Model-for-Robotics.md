---
title: World Model for Robotics
description: 能够预测未来视觉状态或生成子目标图像，为机器人策略提供视觉规划的生成模型
tags:
  - embodied-ai
  - world-model
  - vla
  - video-generation
created: 2026-07-28
---

# World Model for Robotics

World Model for Robotics 是指能够**预测机器人环境未来状态**的生成模型，常用于生成子目标图像或进行视觉规划。

## Core Idea

世界模型接收当前观察和语言指令，输出未来期望的视觉状态。这些预测图像可以作为 VLA 的条件输入，提供比语言更具体的任务规格。

## Architecture

- 基于大规模图像/视频生成模型初始化（如 BAGEL、Stable Diffusion）
- 输入：当前观察图像 + 子任务指令 + 元数据
- 输出：未来子目标图像

## Training Data

- 机器人轨迹中的未来帧
- 人类 egocentric 视频
- 网络视频和图像编辑数据

## Applications

- **Subgoal Image Conditioning**：为 VLA 生成近期目标图像
- **Visual Planning**：生成长程任务的中间视觉目标
- **Cross-embodiment Transfer**：生成目标机器人视角下的合理子目标

## Relationship to VLA

世界模型不直接输出动作，而是为动作策略提供视觉目标。VLA 负责将这些目标转化为控制信号。

## Related Concepts

- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]] — 世界模型的主要应用
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 使用世界模型输出的策略
- [[Mixture-of-Experts]] — 大规模世界模型常用架构

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 使用 BAGEL 初始化的轻量 world model 生成多视角子目标图像
