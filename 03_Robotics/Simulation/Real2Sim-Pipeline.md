---
title: "Real2Sim Pipeline"
description: "将真实场景自动转换为仿真就绪资产的工作流，涉及分割、修复、重建与姿态对齐"
tags: [concept, robotics, simulation, real2sim, 3dgs, automation]
created: 2026-08-03
---

# Real2Sim Pipeline

Real2Sim 管线指从真实世界数据（照片/视频）自动生成可仿真交互场景的工作流，是 sim-to-real 闭环的前置步骤。

## 标准流程

```
RGB 图像
  → 物体分割 (Grounding DINO + SAM)
  → 背景修复 (LaMa)
  → 3D 重建 (3DGS / Mesh)
  → 物理属性绑定
  → 姿态对齐
  → 仿真就绪资产
```

## 关键组件

| 步骤 | 方法 | 作用 |
|------|------|------|
| 物体检测 | Grounding DINO | 开放词汇检测，无需预定义物体类别 |
| 精细分割 | SAM / HQ-SAM | 从检测框生成像素级 mask |
| 背景修复 | LaMa (FFC) | 移除目标物体后自然填补背景 |
| 3D 重建 | SAM-3D / AnySplat | 从单张或多张 RGB 生成 3DGS/Mesh |
| 物理仿真 | 3DGS 绑定到刚体 | 实现可交互动态场景 |

## 工程价值

- **降低场景构建门槛**: 从数天人工建模降至分钟级自动生成
- **大规模数据生成**: 自动生成无限多样化场景用于 VLA 预训练
- **sim-to-real 闭环**: 真实→仿真→训练→部署，加速策略迭代

## 局限性

- 透明/反光物体 3DGS 重建质量差
- 动态物体（液体/布料）尚不支持
- 重建精度直接影响 sim-to-real 迁移效果

## 相关概念

- [[04_Embodied-AI/Sim2Real/3d-gaussian-splatting-simulator|3DGS Simulator]]
- [[01_Fundamentals/ML/Fast-Fourier-Convolution|Fast Fourier Convolution]] — LaMa 核心算子
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]]

## 来源

- [[05_Papers/notes/gs-playground|GS-Playground]] — 端到端自动化 Real2Sim 工作流
