---
title: "Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks"
description: "将 Grounding DINO 与 SAM 组合，实现任意文本驱动的开放世界检测与分割，并可串联其他视觉专家模型完成更复杂任务。"
tags: ["分割", "Grounding-DINO", "SAM", "data-processing", "开放词汇", "视觉基础模型"]
created: 2026-07-28
---

# Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks

## 基本信息

- **作者**: Tianhe Ren, Shilong Liu, Ailing Zeng, Jing Lin, Kunchang Li, He Cao 等 (IDEA & Community)
- **发表**: 2024-01
- **链接**: https://arxiv.org/abs/2401.14159
- **代码/演示**: https://github.com/IDEA-Research/Grounded-Segment-Anything

![[99_Attachments/papers/images/grounded-sam/f28660ba8708e85407d9c360bd06046d7d188a7dce4e41772837856e8e16dc4a.jpg]]

## 研究背景与动机

- 开放世界视觉感知（自动驾驶、机器人导航、安防）需要能根据任意文本指令定位并理解图像区域的模型。
- 已有三条路线各有短板：统一模型数据覆盖不足；LLM 控制器依赖语言模型能力；专家模型各自为政。
- 开放集分割数据稀缺、标注成本高，而开放集检测数据更易获取，且 SAM 已证明在 box 提示下能生成高质量 mask。

## 核心贡献/方法

### 1. Grounded SAM 基础流水线

- **输入**: 图像 + 任意文本提示（类别词、短语、caption）。
- **Grounding DINO**: 开放词汇检测器，根据文本输出目标 bounding box。
- **SAM**: 以这些 box 作为 prompt，生成像素级 mask。
- 本质上是 **training-free 的模型组装**，把检测与分割解耦，规避开放集分割数据稀缺问题。

### 2. 扩展应用（模型组装）

- **RAM-Grounded-SAM / BLIP-Grounded-SAM**: 用图像打标/caption 模型自动生成文本输入，实现全自动图像标注。
- **Grounded-SAM-SD**: 将 Grounded SAM 的 mask 与 Stable Diffusion Inpainting 结合，做可控图像编辑（替换、擦除、修改）。
- **Grounded-SAM-OSX**: 用文本指定某个人（如“戴墨镜的男人”），再调用 OSX 做实例级全身姿态/表情恢复。
- 还可替换更快/更高质量的 SAM 变体（FastSAM、MobileSAM、HQ-SAM）或接入跟踪模型（DEVA）。

## 实验与结论

- **SegInW zero-shot benchmark**（25 个野外分割数据集）:
  - Grounding DINO-Base + SAM-Huge 达到 **48.7 mean AP**。
  - 优于 UNINEXT、OpenSeeD、X-Decoder 等统一开放集分割模型。
- **关键结论**: 将强大的开放集检测器与可提示分割器组合，可在零样本开放集分割上取得领先性能。

## 个人思考

- **工程价值高**: 完全 training-free，直接调用现有权重即可落地，适合快速构建数据标注、图像编辑、机器人感知原型。
- **在 LingBot 中的用途**: 可作为 **data-processing** 模块，自动从视频/图像中按文本指令生成 mask，为 VLA / World Model 提供低成本稠密标注。
- **潜在短板**:
  - 推理是两阶段串行，实时性受限；可用 FastSAM/MobileSAM 加速。
  - Grounding DINO 的检测质量决定 SAM mask 上限，对细长、遮挡、小目标仍可能出错。
  - 文本提示需要人工设计或依赖 RAM/BLIP 自动生成，类别歧义时控制精度不足。
- **可扩展方向**: 接入 SAM2 做视频级 mask tracking，或结合生成模型做数据增强。

## 相关论文

- [[02_AI/VLM/Grounding-DINO|Grounding DINO]]: 开放词汇目标检测器，输出 text-conditioned box。
- [[02_AI/VLM/segment-anything-model|SAM]]: 可提示分割模型，支持 point/box/text mask 生成。
- [[RAM]]: 图像标签模型，用于自动生成 Grounded SAM 的文本输入。
- [[BLIP]]: 图像 caption 模型，同样可作为自动标注前端。
- [[HQ-SAM]]: 高质量 SAM 变体，可提升 mask 边界精度。

## 原文

[[05_Papers/articles/grounded-sam|grounded-sam]]
