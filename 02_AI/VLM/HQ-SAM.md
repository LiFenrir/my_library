---
title: "HQ-SAM"
description: "提升 SAM 分割边界质量的高质量分割模型变体"
tags: [concept, ai, computer-vision, segmentation]
created: 2026-07-31
---

# HQ-SAM

**核心定义**：HQ-SAM（High-Quality SAM）是在 SAM 基础上改进的分割模型，专注于提升分割掩码的边界精度，尤其适用于对 mask 质量要求更高的下游任务。

## 关键改进

- 在 SAM 架构中引入高质量 token 与额外的细节分支；
- 显式优化边界区域，减少锯齿与模糊；
- 保持 SAM 的提示接口与零样本迁移能力。

## 应用场景

- 需要高精度边界的图像编辑；
- 机器人操作中的精细物体掩码提取；
- 与 Grounding DINO 组合提升 Grounded SAM 输出质量。

## 与其他概念的关系

- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — HQ-SAM 的基座模型
- [[02_AI/VLM/grounded-sam|Grounded SAM]] — 可替换 SAM 为 HQ-SAM 提升边界质量

## 来源

- [[05_Papers/articles/grounded-sam|Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks]]
