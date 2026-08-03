---
title: "Segment Anything"
description: "Meta 提出的图像分割基础模型，通过 promptable 任务、SAM 模型与 SA-1B 数据集实现零样本分割能力。"
tags:
  - 分割
  - SAM
  - data-processing
  - foundation-model
  - computer-vision
created: 2026-07-28
---

# Segment Anything

## 基本信息
- **作者**: Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland 等 (Meta AI Research, FAIR)
- **链接**: https://arxiv.org/abs/2304.02643
- **项目主页**: https://segment-anything.com
- **代码**: https://github.com/facebookresearch/segment-anything (Apache 2.0)
- **发表**: ICCV 2023 / arXiv 2023

![[99_Attachments/papers/images/segment-anything/e19cba32735316bcb9038df70dfb5c1210b60dc545b0a3ca4c119842cda4d7e2.jpg]]

## 研究背景与动机

传统分割任务依赖特定数据集和标注，难以像 NLP 大模型那样通过 prompt 泛化到新任务。

- **问题 1**: 分割任务缺乏统一的基础任务定义，无法像 next-token 预测那样支撑大规模预训练。
- **问题 2**: 互联网上分割 mask 数据稀缺，无法直接爬取 web-scale 数据。
- **问题 3**: 现有交互式分割模型多针对特定场景优化，通用性和可组合性不足。

核心目标：构建图像分割领域的 foundation model，使其通过 prompt 工程零样本迁移到多种下游任务。

## 核心贡献

### 1. Promptable Segmentation 任务
- 给定任意提示（点、框、mask、文本），返回一个合理的分割 mask。
- 即使提示存在歧义（如点落在衬衫上，可能指衬衫或人），也至少输出一个有效 mask。
- 作为预训练目标和下游任务统一接口。

### 2. Segment Anything Model (SAM)
- **Image Encoder**: MAE 预训练的 ViT，一次性提取图像 embedding。
- **Prompt Encoder**: 编码点、框、mask、文本等稀疏或密集提示。
- **Lightweight Mask Decoder**: 双向 cross-attention 的 Transformer decoder，50ms 内在浏览器中生成 mask。
- **歧义感知**: 单次提示输出 3 个 mask（整体/部分/子部分），并预测 IoU 置信度排序。

### 3. 数据引擎与 SA-1B 数据集
- 三阶段数据引擎：辅助人工标注 → 半自动标注 → 全自动标注。
- SA-1B 包含 1100 万张授权隐私保护图像，11 亿个高质量 mask。
- 规模是此前最大分割数据集 Open Images 的 400 倍（mask 数量）。

## 模型架构

```
输入图像
    ↓
Image Encoder (ViT-H/L/B) → 64×64 image embedding
    ↓
Prompt Encoder (点/框/mask/文本) → prompt tokens
    ↓
Lightweight Mask Decoder (2 层 Transformer)
    ↓
3 个候选 mask + IoU 置信度
```

### 关键设计
- **解耦推理成本**: 重 encoder 只跑一次，提示相关计算极轻量。
- **歧义处理**: 用 multiple choice learning 训练，只对最低 loss 的 mask 回传梯度。
- **文本提示**: 通过 CLIP 文本编码器提供 embedding（实验性）。

## 实验与结论

### 零样本迁移任务
1. **单点有效 mask**: 在 23 个多样化数据集上，SAM 在 16 个上超过 RITM；人工评分显著优于基线。
2. **边缘检测**: 在 BSDS500 上无需训练即可生成合理边缘图，R50 超越传统 zero-shot 方法。
3. **目标候选框**: 在 LVIS v1 上 AR@1000 接近甚至超过 ViTDet-H。
4. **实例分割**: 用 ViTDet 检测框作为 prompt，COCO/LVIS mask AP 接近全监督 ViTDet，人工评分更优。
5. **文本到 mask**: 通过 CLIP 对齐实现简单文本提示分割（概念验证）。

### 消融实验
- 仅使用全自动生成的 mask 训练，性能与三阶段数据相当（差距 ~0.5 mIoU）。
- 使用约 10% 数据（100 万张图像）即可达到接近完整数据集的效果。
- ViT-H 相比 ViT-L 提升边际递减，小模型在特定场景更实用。

## 局限性与后续方向

论文自述局限：
- 可能丢失精细结构，偶尔产生小的不连通碎片。
- 边界锐度不如专门“放大”优化的方法（如 FocalClick）。
- 多轮交互分割非其优化目标，高 IoU 场景下不如专用交互模型。
- 整体实时性受限于重型 image encoder。
- 文本提示为初步探索，鲁棒性有限。

> 我的理解：SAM 的价值在于将分割从“任务专用模型”转变为“可组合的基础组件”。在具身智能和机器人场景中，SAM 可作为视觉前端快速提取物体 mask，为 VLA、3D 重建、抓取等下游模块提供低成本的分割输入。

## 与 LingBot 关联

- **视觉感知模块**: 可用于机器人场景中的物体分割与 ROI 提取。
- **数据标注**: 自动生成训练数据 mask，降低人工标注成本。
- **与 VLA 结合**: 作为视觉 grounding 的前置工具，将语言/点/框指令转化为 mask。

## 相关概念
- [[foundation-model]]
- [[computer-vision]]
- [[image-segmentation]]
- [[prompt-engineering]]
- [[02_AI/VLM/Vision-Transformer|Vision Transformer]]
- [[MAE]]
- [[CLIP]]

## 原文

[[05_Papers/articles/segment-anything|segment-anything]]
