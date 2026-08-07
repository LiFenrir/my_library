---
title: "Promptable Segmentation"
description: "通过点、框、文本等提示灵活指定图像中分割目标的通用分割范式"
tags: [concept, ai, computer-vision, segmentation]
created: 2026-07-29
---

# Promptable Segmentation

**核心定义**：Promptable Segmentation 是一种通用图像分割范式，模型接受各种提示（点、框、掩码、文本）并输出对应目标的分割掩码，支持零样本迁移到多种下游任务。

## 代表模型

- **SAM (Segment Anything Model)**：Meta 提出的分割基础模型，在 11M 图像、1B+ 掩码上训练
- **Grounded SAM**：结合 Grounding DINO 的开放词汇检测与 SAM 的分割能力

## 提示类型

| 提示 | 说明 |
|------|------|
| 点 | 点击前景/背景 |
| 边界框 | 框选目标 |
| 掩码 | 初始粗略掩码 |
| 文本 | 开放词汇描述 |

## 在机器人中的应用

- 物体掩码获取
- 手部/机器人部件分割
- 开放词汇检测-分割（如 Grounded SAM）
- 与人类或语言模型交互的感知接口

## 与其他概念的关系

- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — 文本提示分割需要语言理解
- [[02_AI/VLM/segment-anything-model|Segment Anything Model]] — promptable segmentation 的代表实现
- [[02_AI/VLM/grounded-sam|Grounded SAM]] — 文本提示分割的组装式实现
- [[02_AI/General/Model-in-the-Loop-Data-Engine|Model-in-the-Loop Data Engine]] — 为 promptable segmentation 模型构建大规模训练数据
- [[03_Robotics/Perception/index|Robot Perception]] — 分割是机器人感知的基础能力
- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — SAM 可用于手部分割
- [[02_AI/General/Foundation-Model|Foundation Model]] — promptable segmentation 是构建 CV 基础模型的任务范式

## 补充：来自 [[05_Papers/articles/segment-anything|Segment Anything]]

### 任务形式化

Promptable Segmentation 任务的精确定义：给定任意提示（prompt），模型必须返回一个**有效**的分割掩码。这里的“有效”指即使提示存在歧义（例如一个点落在衬衫上，可能指衬衫或穿衣人），输出也至少是其中一个合理对象的掩码。

该任务同时承担两个角色：
1. **预训练目标**：通过模拟提示序列（点、框、掩码等）训练模型。
2. **零样本迁移接口**：下游任务通过设计合适的提示即可调用模型，无需重新训练。

### 预训练算法

从交互式分割借鉴而来，但目标不同：交互式分割追求在用户给出足够提示后得到正确掩码；而 promptable segmentation 要求**对任何提示都能立即给出有效掩码**，即使提示有歧义。因此需要专门的建模与损失设计。

### 零样本迁移机制

预训练使模型具备对任意提示作出合理响应的能力。下游任务通过构造合适的提示实现零样本迁移，例如：
- 将目标检测器的输出框作为提示 → 实例分割
- 将规则点阵作为提示 → 物体候选区域生成
- 将文本描述作为提示 → 文本到掩码分割

### 与相关任务的区别

| 任务/范式 | 特点 | 与 Promptable Segmentation 的区别 |
|-----------|------|-----------------------------------|
| 交互式分割 | 以人类用户为中心，逐步修正 | Promptable 更强调任意提示下的即时有效输出 |
| 多任务分割 | 固定任务集合联合训练 | Promptable 在推理时可通过提示组合完成新任务 |
| 语义/实例/全景分割 | 预定义类别或对象定义 | Promptable 通过提示指定目标，类别不固定 |

### 提示与组合的力量

Prompting 和 composition 使单一模型能够以可扩展方式完成设计时未预见到的任务。Promptable Segmentation 模型可作为更大系统中的可靠组件，例如：
- 与检测器组合 → 实例分割
- 与 3D 重建模型组合 → 单目 RGB-D 物体重建
- 与眼动追踪设备组合 → 基于注视点的分割

## 来源

- [[05_Papers/articles/segment-anything|Segment Anything]]
- [[05_Papers/articles/grounded-sam|Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks]]
