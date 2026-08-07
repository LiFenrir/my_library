---
title: "机器人数据质量筛选"
description: "机器人训练数据的三层质量过滤：pipeline 内部校验、统计异常剔除、VLM 语义一致性审核。"
tags: [robotics, data-quality, dataset, embodied-ai]
created: 2026-08-06
---

# 机器人数据质量筛选

对合成或采集的机器人演示数据进行分层过滤，去除不可行、不稳定或语义不一致的样本。

## 三层过滤

### L1 — Pipeline-internal

在数据生成/采集过程中即时标记：
- IK 求解失败
- 自碰撞
- 动作越界
- 工作空间覆盖不足

### L2 — Statistical

整条轨迹层面的异常检测：
- 极值动作
- 帧间不连续/跳变
- 无效帧比例过高
- 轨迹长度异常

### L3 — VLM Consistency

用视觉-语言模型审核合成视频：
- 渲染机器人动作是否与原始操作意图一致
- 物体/场景语义是否保持
- 是否存在明显视觉伪影

## 应用建议

- 质量筛选应放在数据生成 pipeline 的固定环节，而非后处理可选步骤
- 不同数据源/形态可能需要不同的阈值
- 保留过滤日志，便于后续分析 bias

## 相关

- [[05_Papers/notes/ego2robot|ego2robot]]
- [[04_Embodied-AI/Data-and-Evaluation/Ego-to-Robot-Synthesis|Ego-to-Robot Synthesis]]
