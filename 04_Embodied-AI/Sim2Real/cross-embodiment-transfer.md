---
title: "Cross-Embodiment Transfer"
description: "将在一种机器人形态上学到的策略或表示迁移到另一种形态的能力"
tags: [concept, embodied-ai, sim2real, transfer-learning, robot-learning]
created: 2026-07-31
---

# Cross-Embodiment Transfer

**核心定义**：Cross-Embodiment Transfer 指将在一种机器人形态（embodiment）上学习得到的策略、表示或世界模型，迁移到另一种形态不同的机器人上的能力。它是解决机器人数据稀缺与泛化问题的关键方向。

## 为什么需要

- 不同机器人（机械臂、轮式、足式、无人机）的关节结构、动作空间、传感器配置差异巨大；
- 为每种形态单独收集数据并训练策略成本高昂；
- 希望利用互联网上大量异构机器人或人类操作视频学习通用能力。

## 关键思路

1. **动作无关表示**：从视频中学习不依赖具体执行器的潜在动作表示；
2. **Latent Action**：在紧凑潜在空间中建模动作，弱化原始电机命令的差异；
3. **统一世界模型**：训练一个能处理多种 embodiment 输入/输出的世界模型；
4. **Domain Randomization**：在仿真中随机化机器人形态参数以增强泛化。

## 代表工作

- Motus：unified latent action world model
- 基于人类视频学习机器人操作的跨形态迁移
- 大规模跨机器人数据联合训练

## 优缺点

- **优点**：提高数据利用效率；促进策略在新机器人上的快速部署。
- **局限**：形态差异大时迁移仍困难；潜在动作与真实执行器对齐需要额外机制。

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/latent-action|Latent Action]] — 跨形态迁移的常用表示
- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — 统一的动作-视频预测模型
- [[04_Embodied-AI/Sim2Real/Domain-Randomization|Domain Randomization]] — 增强跨形态泛化的训练技术
- [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 从人类数据向机器人形态迁移

## 来源

- [[05_Papers/articles/motus|Motus: A Unified Latent Action World Model]]
