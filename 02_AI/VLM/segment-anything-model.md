---
title: Segment Anything Model
description: Meta 提出的 promptable segmentation 基础模型，通过图像编码器、提示编码器与轻量掩码解码器实现零样本分割
tags:
  - concept
  - ai
  - computer-vision
  - segmentation
  - foundation-model
  - SAM
created: 2026-07-30
---

# Segment Anything Model (SAM)

**核心定义**：SAM 是 Meta 提出的图像分割基础模型，接受点、框、掩码或文本等提示，输出对应目标的分割掩码，支持零样本迁移到多种下游任务。

## 动机

构建一个面向图像分割的“基础模型”：在大规模多样数据上预训练，通过提示工程（prompt engineering）零样本泛化到新数据分布和新任务。

## 模型架构

SAM 由三个解耦组件组成，实现“图像编码一次、多次提示实时解码”：

### 1. 图像编码器（Image Encoder）

- 使用 MAE 预训练的 Vision Transformer（ViT），最小化修改以处理高分辨率输入。
- 每张图像只运行一次，输出图像嵌入（image embedding）。
- 图像编码器的计算成本可以被多次提示摊销。

### 2. 提示编码器（Prompt Encoder）

支持稀疏提示和密集提示两类：

| 提示类型 | 表示方式 |
|----------|----------|
| 点（point） | 位置编码 + 前景/背景可学习嵌入 |
| 框（box） | 左上角/右下角位置编码 + 角点可学习嵌入 |
| 文本（text） | CLIP 文本编码器输出的嵌入 |
| 掩码（mask） | 卷积下采样后与图像嵌入逐元素相加 |

### 3. 掩码解码器（Mask Decoder）

- 轻量级 Transformer decoder 变体，结合图像嵌入与提示嵌入。
- 每个 decoder 层包含四步：
  1. 提示 token 的自注意力
  2. 提示 token → 图像嵌入的交叉注意力
  3. 逐点 MLP 更新 token
  4. 图像嵌入 → 提示 token 的交叉注意力（用提示信息更新图像嵌入）
- 输出 token 经 MLP 映射为动态线性分类器，计算每个位置的前景概率。
- 图像嵌入上采样后与输出 token 结合生成最终掩码。

## 歧义感知设计

单输出模型在歧义提示下会对多个有效掩码取平均，导致结果模糊。SAM 改为**单次提示预测多个输出掩码**（通常 3 个）：

- 3 个输出足以覆盖常见嵌套层级：整体（whole）、部分（part）、子部分（subpart）。
- 训练时只对损失最小的掩码反向传播。
- 每个掩码伴随一个置信度分数（估计 IoU），用于排序。

## 效率

- 图像编码器计算重但只跑一次。
- 提示编码器 + 掩码解码器在浏览器 CPU 上约 **50ms**，支持实时交互式提示。

## 损失与训练

- 掩码预测损失：focal loss 与 dice loss 的线性组合。
- 训练时使用几何提示的混合，并模拟交互式设置：每个掩码随机采样 11 轮提示。
- 文本提示通过 CLIP 图像嵌入间接训练：训练时用 CLIP 图像嵌入作为首个提示，推理时替换为 CLIP 文本嵌入。

## 基础模型视角

SAM 符合“在广泛数据上大规模训练、可适配多种下游任务”的基础模型定义，但有两个特点：

1. **范围聚焦**：只针对图像分割这一计算机视觉子问题，而非通用视觉。
2. **监督训练为主**：虽然图像编码器用自监督 MAE 初始化，但核心能力主要来自大规模有监督训练（通过数据引擎扩展标注）。

## 局限性

- 可能丢失精细结构。
- 偶尔产生小的不连通伪影。
- 边界不如专门“zoom-in”方法锐利。
- 在提供大量点击点的传统交互式分割场景下，专用方法可能 IoU 更高。
- 文本到掩码能力尚处探索阶段，鲁棒性有限。

## 与其他概念的关系

- [[02_AI/VLM/promptable-segmentation|Promptable Segmentation]] — SAM 是该范式的代表实现
- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — 文本提示依赖 VLM 的跨模态对齐
- [[02_AI/General/Model-in-the-Loop-Data-Engine|Model-in-the-Loop Data Engine]] — SAM 的能力依托数据引擎生成的大规模掩码
- [[02_AI/General/Foundation-Model|Foundation Model]] — SAM 是计算机视觉领域的基础模型尝试

## 来源

- [[05_Papers/articles/segment-anything|Segment Anything]]
