---
title: "World Models"
description: "世界模型综述：基于内部世界模型进行预测、推理与决策。"
tags: ["世界模型", "World Models", "JEPA", "自监督学习"]
created: 2026-07-15
---

# World Models

## 基本信息
- **作者**: David Ha (Google Brain), Jürgen Schmidhuber (IDSIA, NNAISENSE, KAIST)
- **链接**: https://worldmodels.github.io
- **发表**: NeurIPS 2018 Workshop
- **代码**: https://github.com/ctallec/world-models
- **本地 PDF**: `99_Attachments/papers/pdfs/world-models.pdf`

## 研究背景与动机

人类基于有限感官发展出对世界的内部心智模型，决策和行动都基于这个内部模型。为处理日常生活中海量信息，大脑学习了对信息时空方面的抽象表示。

在强化学习中，智能体同样受益于对过去和现在状态的良好表示，以及对未来的预测模型。然而传统无模型 RL 方法通常只使用小型神经网络，因为信用分配问题使训练大型模型困难。

本文提出将智能体分为**大型世界模型**和**小型控制器模型**：先以无监督方式训练大型神经网络学习环境模型，然后训练小型控制器使用该世界模型执行任务。

![[99_Attachments/papers/images/world-models/272ae0ecea227f9b33e746bb5e714965183ba748f0ef8cd1b3e23ef01ae8ded6.jpg]]

## 核心方法

### 智能体架构

智能体由三个紧密协作的组件组成：

![[99_Attachments/papers/images/world-models/cf19e655575609115dfcf0984b1c85a79580471b36dcea9fdd0a2201463947a1.jpg]]

**1. Vision (V) Model — VAE**
- 将高维输入观测（通常是 2D 图像帧）压缩为小型潜在向量 $z$
- 使用变分自编码器学习每帧的抽象压缩表示

**2. Memory (M) Model — MDN-RNN**
- 预测 V 模型未来产生的 $z$ 向量
- 由于环境通常是随机的，训练 RNN 输出概率密度函数 $p(z)$ 而非确定性预测
- 近似为高斯混合分布，建模 $P(z_{t+1} | a_t, z_t, h_t)$
- 采样时可调整温度参数 $\tau$ 控制模型不确定性

**3. Controller (C) Model**
- 基于 V 和 M 创建的表示决定采取什么动作
- 非常紧凑的简单策略
- 仅使用世界模型提取的特征作为输入

![[99_Attachments/papers/images/world-models/456addd2afef86fc25d5b30f89f158ce99837cd9a8158de65834d68333db224d.jpg]]

### 训练流程

1. **收集数据**：从实际游戏环境中记录观测序列
2. **训练 V 模型**：VAE 学习压缩每帧图像为潜在向量 $z$
3. **训练 M 模型**：MDN-RNN 学习预测未来的 $z$ 向量
4. **训练 C 模型**：使用世界模型作为环境训练控制器

### 在梦境中训练

关键创新：可以在智能体自己的**幻觉梦境**中完全训练智能体，然后将策略迁移回实际环境。

- 世界模型模仿完整环境
- 小控制器使训练算法专注于小搜索空间上的信用分配问题
- 不牺牲大世界模型的容量和表达能力

## 实验结果

**环境**：OpenAI Gym（CarRacing, VizDoom 等）

**主要发现**：
- 世界模型可以快速以无监督方式训练
- 使用世界模型特征作为输入，可训练非常紧凑的策略解决任务
- 在梦境中训练的策略可成功迁移到实际环境
- 小控制器 + 大世界模型的分工使训练高效

## 核心贡献

1. **世界模型-控制器分离**：将大型 RNN 世界模型与小型控制器解耦，解决信用分配瓶颈
2. **梦境训练**：在生成的环境模拟中训练策略，大幅降低样本复杂度
3. **无监督表示学习**：VAE + MDN-RNN 学习压缩的时空表示
4. **温度控制**：通过调整 MDN-RNN 的温度参数控制模型不确定性，有助于探索

## 与后续工作的关系

本文是模型-based RL 的重要里程碑，影响了后续多个方向：
- **Dreamer 系列**：在此基础上引入更稳定的训练方法和更复杂的环境
- **World Models for Robotics**：将思想扩展到机器人领域
- **Model-Based Policy Optimization**：结合模型-based 和无模型方法

## 个人思考

- **历史意义**：2018 年的开创性工作，将 Schmidhuber 1990-2015 年的 RNN 世界模型思想简化并实验验证
- **核心洞见**：将智能体分为"大脑"（世界模型）和"反射"（控制器）符合认知科学原理
- **局限性**：
  - VAE 压缩可能丢失关键信息
  - MDN-RNN 对复杂环境的建模能力有限
  - 仅在简单游戏环境验证
- **现代启示**：
  - 与当前世界模型研究（如 DreamerV3, UniWorld）一脉相承
  -  latent 空间规划的思想在 VLA 模型中仍有价值
  - 3DGS/NeRF 等新型表示可替代 VAE 作为视觉编码器


## 原文

[[05_Papers/articles/world-models|world-models]]
