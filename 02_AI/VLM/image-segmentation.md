---
title: "Image Segmentation"
description: "将图像划分为具有语义或实例意义的区域的计算机视觉任务"
tags: [concept, ai, computer-vision, segmentation]
created: 2026-07-31
---

# Image Segmentation

**核心定义**：Image Segmentation（图像分割）是将图像中的每个像素分配到某个类别（语义分割）、某个对象实例（实例分割）或同时考虑两者（全景分割）的计算机视觉任务。

## 主要类型

| 类型 | 说明 |
|------|------|
| 语义分割 | 每个像素对应类别，不区分实例 |
| 实例分割 | 区分不同对象实例 |
| 全景分割 | 语义分割与实例分割的统一 |
| 交互式分割 | 基于用户提示逐步修正 |
| Promptable Segmentation | 通过任意提示（点/框/文本）获得目标掩码 |

## 与机器人的关系

分割结果为机器人操作提供物体边界、可抓取区域和场景理解基础。

## 与其他概念的关系

- [[02_AI/VLM/promptable-segmentation|Promptable Segmentation]] — 通用分割范式
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — 分割基础模型
- [[02_AI/VLM/computer-vision|Computer Vision]] — 分割所属领域

## 来源

- [[05_Papers/articles/segment-anything|Segment Anything]]
