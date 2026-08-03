---
title: "pi0.7 通用知识提取总结"
description: "从 pi0.7 论文笔记中提取的通用知识沉淀方案与输出文件清单。"
tags: [summary, knowledge-extraction, pi0-7]
created: 2026-07-28
---

# pi0.7 通用知识提取总结

## 提取原则

- **通用 vs 具体分离**：把 flow matching 等通用生成模型方法放到 `01_Fundamentals/ML/generative-models`，把 VLA 架构、上下文条件、世界模型、泛化等放到 `04_Embodied-AI`。
- **以概念为单位**：每篇笔记聚焦一个可复用的知识点，而不是复述 pi0.7 实验细节。
- **建立链接**：笔记之间用 `[[...]]` 双向链接，并回链到 [[05_Papers/articles/pi0-7|pi0.7 论文笔记]]。

## 输出文件清单

| 目标路径 | 知识主题 |
|---|---|
| `01_Fundamentals/ML/generative-models/flow-matching.md` | Flow Matching 作为通用生成建模方法，以及 CFG 在条件生成中的作用 |
| `04_Embodied-AI/VLA/VLA-architecture.md` | VLA 通用架构：VLM 主干、视觉历史编码、action expert、知识绝缘、RTC、control mode |
| `04_Embodied-AI/VLA/multimodal-context-conditioning.md` | 多模态 prompt（子任务语言、子目标图像、episode metadata、control mode）与 dropout/CFG |
| `04_Embodied-AI/World-Model/subgoal-image-world-model.md` | 为 VLA 生成子目标图像的轻量级世界模型：BAGEL 初始化、条件流匹配、异步推理 |
| `04_Embodied-AI/generalization/cross-embodiment-transfer.md` | 零样本跨 embodiment 迁移、形态差距、涌现策略、子目标图像的作用 |
| `04_Embodied-AI/generalization/compositional-task-generalization.md` | 组合任务泛化与语言教练机制，及其蒸馏为高层策略 |
| `04_Embodied-AI/VLA/learning-from-mixed-quality-data.md` | 用 episode metadata 区分数据质量/策略，支持数据规模扩展与 specialist rollout 蒸馏 |

## 关键映射说明

- **Flow matching action expert** 被视为通用生成模型方法，归入 `01_Fundamentals`；VLA 中的具体实现留在 `04_Embodied-AI/VLA/VLA-architecture.md`。
- **VLA 架构**、**多模态上下文条件**、**世界模型**、**泛化/迁移**、**数据规模扩展** 都是具身智能领域的通用概念，因此统一沉淀到 `04_Embodied-AI` 下对应子目录。
- 所有笔记均只写入 `outputs/` 工作区，未修改真实的 `01_Fundamentals/`、`02_AI/`、`03_Robotics/`、`04_Embodied-AI/` 目录。
