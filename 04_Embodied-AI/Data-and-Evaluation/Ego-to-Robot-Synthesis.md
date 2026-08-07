---
title: "Ego-to-Robot 数据合成"
description: "将第一视角人体操作视频转换为机器人训练数据的范式：动作重定向、视觉对齐、质量筛选与跨形态数据统一。"
tags: [embodied-ai, robot-learning, data-synthesis, egocentric-video, cross-embodiment]
created: 2026-08-06
---

# Ego-to-Robot 数据合成

把 egocentric 人体操作视频转换成机器人可训练格式，解决机器人数据采集成本高、多样性不足的问题。

## 核心动机

- 人体视频场景/任务/物体多样性远高于机器人遥操作数据
- 直接训练受 embodiment gap 限制：手 vs 机械臂、自由度、速度、外观均不同
- 目标：提取可迁移的交互规律，作为机器人数据的补充预训练信号

## 典型 Pipeline

1. **动作对齐**：手部关键点 → 机器人末端执行器轨迹
2. **视觉对齐**：分割并去除人手 → 确定机器人 base placement → IK 渲染机器人 → 深度感知合成
3. **质量筛选**：剔除 IK 失败、自碰撞、语义不一致等低质量样本

## 关键设计

- **Camera-Frame Relative EEF**：用相机坐标系下的相对末端执行器动作统一不同相机位姿与机器人形态
- **多形态并行渲染**：同一人体轨迹生成多种机器人 embodiment 的训练样本
- **速度对齐**：按数据源降采样以匹配机器人动作速度分布

## 工程要点

- 手部姿态估计精度决定动作质量
- Base placement 搜索影响 IK 可行性与视觉合理性
- 修复/渲染在遮挡严重时可能产生伪影

## 相关

- [[05_Papers/notes/ego2robot|ego2robot]] — Ego2Robot 论文笔记
- [[04_Embodied-AI/Data-and-Evaluation/Hand-to-Gripper-Retargeting|Hand-to-Gripper Retargeting]]
- [[04_Embodied-AI/Data-and-Evaluation/Camera-Frame-Relative-EEF|Camera-Frame Relative EEF]]
- [[04_Embodied-AI/Data-and-Evaluation/Robot-Data-Quality-Curation|Robot Data Quality Curation]]
- [[03_Robotics/Simulation/Disentangled-Robot-Generalization-Benchmark|Disentangled Generalization Benchmark]]
