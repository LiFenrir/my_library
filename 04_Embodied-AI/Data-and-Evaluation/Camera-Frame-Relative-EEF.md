---
title: "Camera-Frame Relative EEF"
description: "相机坐标系下的相对末端执行器动作表示，用于统一多源相机、多机器人形态的数据动作空间。"
tags: [robotics, action-representation, cross-embodiment, vla]
created: 2026-08-06
---

# Camera-Frame Relative EEF

用相机坐标系表示末端执行器（EEF）的相对位移，替代世界坐标系或机器人 base 坐标系动作表示。

## 为什么需要

- 不同 egocentric 视频源相机内参、位姿未知，世界坐标系动作需要逐视频标定
- 不同机器人形态 base 坐标系不同，难以直接混合训练
- 相机坐标系天然与图像像素对齐，且对机器人 base 位置不敏感

## 表示形式

- 动作 = 当前帧相机坐标系下 EEF 的相对平移 + 相对旋转 + 夹爪开合变化
- 预测目标通常是未来若干步的相对位姿

## 优势

- 统一多源 ego 视频与多机器人形态数据
- 与视觉输入在同一坐标系，便于 VLA 学习
- 对相机/机器人 base 的小扰动更鲁棒

## 局限

- 绝对尺度依赖深度估计或内参
- 远距离/大位移时精度下降
- 需要与真实机器人控制接口做坐标转换

## 相关

- [[05_Papers/notes/ego2robot|ego2robot]]
- [[04_Embodied-AI/Data-and-Evaluation/Ego-to-Robot-Synthesis|Ego-to-Robot Synthesis]]
- [[03_Robotics/Perception/Coordinate-Frames|Coordinate-Frames]]
