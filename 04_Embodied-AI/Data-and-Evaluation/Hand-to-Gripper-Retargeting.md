---
title: "Hand-to-Gripper Retargeting"
description: "将人体手部关键点映射到平行夹爪末端执行器位姿的方法：虚拟指尖、TCP、夹爪宽度与坐标系对齐。"
tags: [robotics, retargeting, manipulation, egocentric-video]
created: 2026-08-06
---

# Hand-to-Gripper Retargeting

把人体手部姿态转换为机器人平行夹爪（parallel-jaw gripper）的 6D 位姿与开合宽度。

## 经典映射

- **虚拟指尖**：食指尖与中指尖的加权混合（如 0.7 : 0.3）
- **TCP**：拇指尖与虚拟指尖的中点
- **夹爪宽度**：拇指尖到虚拟指尖的距离
- **夹爪坐标系**：
  - z 轴：沿夹爪 jaw line（拇指 → 虚拟指尖）
  - y 轴：垂直于 jaw 平面
  - x 轴：approach 方向，由 y × z 得到
- **左右手统一**：通过符号 $s = \pm 1$ 使 z 轴方向一致

## 时序处理

- 对位置/宽度做 Savitzky-Golay 滤波
- 对方向做 Gaussian-weighted SLERP
- 消除单帧检测高频噪声，保留运动结构

## 局限

- 仅适用于平行夹爪，丢失多指灵巧操作信息
- 手部遮挡或姿态估计失败会传递到机器人动作

## 相关

- [[05_Papers/notes/ego2robot|ego2robot]]
- [[04_Embodied-AI/Data-and-Evaluation/Ego-to-Robot-Synthesis|Ego-to-Robot Synthesis]]
