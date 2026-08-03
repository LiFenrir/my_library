---
title: "Latent Frame Injection"
description: "将机器人状态、动作和价值等新模态编码为潜在帧注入视频扩散模型序列的适配方法"
tags: [concept, embodied-ai, world-model, video-generation]
created: 2026-07-29
---

# Latent Frame Injection

**核心定义**：Latent Frame Injection 是一种将新模态（如机器人本体状态、动作块、状态价值）编码为与视频潜在帧同形的张量，并直接插入预训练视频扩散模型序列的方法，从而在不修改架构的情况下将视频模型适配为机器人策略。

## 原理

预训练视频模型原本按时间顺序处理视频帧的潜在表示。Cosmos Policy 将每个新模态也视为一个"潜在帧"：

- 机器人本体状态（如关节角、末端执行器位姿）复制填充为 $H' \times W' \times C'$ 的张量
- 动作块（连续动作序列）同样 reshape 并归一化到 $[-1, +1]$
- 状态价值（标量）复制为同形张量

这些新帧与原始视频帧、多视角图像帧交错排列在扩散序列中。

## 典型序列

对于两台第三人称相机 + 一台腕部相机的机器人，潜在序列可能包含：

1. blank placeholder
2. 当前机器人本体状态
3. 腕部相机图像
4. 第一台第三人称相机图像
5. 第二台第三人称相机图像
6. 动作块
7. 未来机器人本体状态
8. 未来腕部相机图像
9. 未来第一台第三人称相机图像
10. 未来第二台第三人称相机图像
11. 未来状态价值

## 训练目标

通过不同的 conditioning mask，同一模型可同时学习：

- 策略：$p(a, s', V(s') | s)$
- 世界模型：$p(s', V(s') | s, a)$
- 价值函数：$p(V(s') | s, a, s')$

## 优缺点

- **优点**：无需修改视频模型架构、可利用大规模视频预训练、统一策略/世界模型/价值函数
- **缺点/局限**：潜在帧设计依赖具体机器人设置、多模态对齐需要 careful 归一化

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/World-Model|World Model]] — Latent Frame Injection 是视频世界模型适配的一种方式
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 与 Cosmos Policy 相对的策略范式
- [[01_Fundamentals/ML/diffusion-model|Diffusion Model]] — Cosmos Policy 的基础生成模型

## 实现细节补充

### 模态编码与归一化

每个新模态被归一化到 $[-1, +1]$ 后，复制填充为与潜在帧同形的 $H' \times W' \times C'$ 张量：

- 动作块 $\mathbf{a}_{t:t+K}$（形状 $K \times d_{\text{act}}$）flatten 后重复 $(H' \times W' \times C') / (K \times d_{\text{act}})$ 次
- 机器人本体状态（关节角或末端执行器位姿）同样 reshape 并复制
- 状态价值（标量）复制到整个潜在帧

### 多相机视角处理

多视角图像直接在图像序列级别插入。例如两台第三人称相机 + 一台腕部相机的典型潜在序列为：

1. blank placeholder
2. 当前机器人本体状态
3. 腕部相机图像
4. 第一台第三人称相机图像
5. 第二台第三人称相机图像
6. 动作块
7. 未来机器人本体状态
8. 未来腕部相机图像
9. 未来第一台第三人称相机图像
10. 未来第二台第三人称相机图像
11. 未来状态价值

### 模态提取

去噪后的潜在帧不需要 VAE 解码即可提取非图像模态：

- 动作块：对潜在帧中所有复制副本取平均，再反归一化
- 价值：对整个潜在帧取平均，再反归一化到 $[0, 1]$

### 推理时的噪声 schedule 调整

视频生成任务的噪声分布通常偏重低噪声水平，而动作生成需要更高的精度。实践中可：

- 训练时使用 hybrid log-normal-uniform 分布，增加高噪声水平的采样权重
- 推理时设置更高的 $\sigma_{\min}$（如 4 而非 0.002），避免极低信噪比下的不准确预测

## 来源

- [[05_Papers/articles/cosmos-policy|COSMOS POLICY: Fine-Tuning Video Models for Visuomotor Control and Planning]]，第 3、4.1、A.1、A.2.1 节
