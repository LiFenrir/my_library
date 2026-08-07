---
title: "解耦机器人泛化评估"
description: "将机器人策略泛化能力拆分为视觉外观、场景布局、本体形态、任务语义四个独立维度，分别测试。"
tags: [robotics, benchmark, generalization, evaluation]
created: 2026-08-06
---

# 解耦机器人泛化评估

传统 OOD benchmark 常把多种分布偏移混合成一个分数，难以定位失败来源。解耦评估将泛化拆分为独立轴。

## 四个维度

### 1. Visual Appearance

- 背景纹理
- 光照条件
- 机器人/物体颜色

### 2. Scene Layout

- 桌面高度
- 干扰物
- 相机视角偏移

### 3. Embodiment Morphology

- 跨机器人形态零样本迁移
- 通过 IK 对齐初始 EEF 位姿
- 测试动作表示是否真正与形态无关

### 4. Task Semantics

- 未见物体实例
- 指令改写/同义表达

## 价值

- 精确归因：知道模型弱在视觉、空间、本体还是语义
- 指导数据增强：哪类数据对哪类泛化最有帮助
- 避免单一 OOD 分数掩盖真实问题

## 实践建议

- 每个维度独立随机化，其他维度保持训练分布
- 初始位姿对齐对 embodiment 评估至关重要
- 需要足够多样的任务才能区分 semantic vs visual 收益

## 相关

- [[05_Papers/notes/ego2robot|ego2robot]]
- [[04_Embodied-AI/Data-and-Evaluation/Camera-Frame-Relative-EEF|Camera-Frame Relative EEF]]
