---
title: "Video Foundation Model for Robotics"
description: "将大规模预训练视频生成模型作为机器人策略初始化，利用其时空先验进行视觉运动控制与规划的范式"
tags: [concept, embodied-ai, video-generation, robot-policy, world-model]
created: 2026-07-30
---

# Video Foundation Model for Robotics

**核心定义**：Video Foundation Model for Robotics 是指将大规模预训练视频生成模型（如 Cosmos-Predict2、Wan2.1）作为机器人策略的初始化或 backbone，利用其从互联网视频中学到的时空因果性、隐式物理与运动模式来完成视觉运动控制与规划的范式。

## 为什么使用视频基础模型

与从静态图像-文本对预训练的视觉-语言模型（VLM）不同，视频基础模型从数百万视频中学习：

- **时间因果性**：物体如何随时间演化
- **隐式物理**：碰撞、重力、形变等物理规律
- **运动模式**：人手/物体常见的运动轨迹

这些时空先验对机器人低层控制尤为重要。

## 与 VLA 范式的对比

| 维度 | Vision-Language-Action (VLA) | Video-based Robot Policy |
|------|------------------------------|--------------------------|
| 预训练数据 | 静态图像-文本对 | 互联网视频 |
| 核心能力 | 语义理解、概念泛化 | 时空动态、物理直觉、动作多模态 |
| 架构修改 | 通常需要新增 action head / action expert | 可无架构修改，直接微调视频模型 |
| 典型代表 | RT-2, OpenVLA, π0, CogVLA | Cosmos Policy, UVA, Video Policy, UWM |
| 优势场景 | 语言指令、语义泛化 | 长程时序一致性、高动作多模态、精细操作 |

## 核心适配方法

### 1. 分阶段训练（Two-stage）

先在机器人数据上微调视频模型，再训练独立的动作模块从生成帧中预测动作：

- 代表：UVA, Video Policy
- 优点：模块化，动作模块可单独优化
- 缺点：多阶段优化复杂，可能损失视频先验

### 2. 统一视频-动作模型（Unified）

从头训练联合建模视频帧与动作的生成模型：

- 代表：UWM, Unified Video Action Model
- 优点：端到端
- 缺点：无法利用预训练视频模型，需要大量数据

### 3. 单阶段视频模型微调（Single-stage Fine-tuning）

直接将动作、未来状态、价值编码为潜在帧注入预训练视频扩散模型：

- 代表：[[04_Embodied-AI/World-Model/latent-frame-injection|Cosmos Policy]]
- 优点：无架构修改、保留预训练先验、统一策略/世界模型/价值函数
- 缺点：潜在帧设计依赖具体机器人平台

## 能力扩展

- **直接策略（Direct Policy）**：生成动作块直接执行
- **未来状态预测**：作为世界模型想象动作执行后的场景
- **价值预测**：评估未来状态的成功率，支持规划
- **从经验学习（Learning from Rollouts）**：利用策略 rollout 数据精炼世界模型与价值函数

## 优缺点

- **优点**：可利用大规模无动作标注视频预训练；天然建模动作多峰分布；统一生成框架支持策略、世界模型、价值函数
- **缺点/局限**：推理 latency 高于 VLA；需要 careful 的噪声 schedule 调整；对 rollout 数据分布敏感

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — 基于 VLM 的机器人策略范式
- [[04_Embodied-AI/World-Model/latent-frame-injection|Latent Frame Injection]] — 将视频模型适配为策略的具体机制
- [[04_Embodied-AI/World-Model/World-Model|World Model]] — 视频基础模型可作为世界模型使用
- [[04_Embodied-AI/World-Model/model-based-planning-for-robotics|Model-Based Planning for Robotics]] — 利用视频模型进行规划
- [[01_Fundamentals/ML/diffusion-model|Diffusion Model]] — 视频基础模型常用的生成框架

## 来源

- [[05_Papers/articles/cosmos-policy|COSMOS POLICY: Fine-Tuning Video Models for Visuomotor Control and Planning]]，第 1、2、4 节
