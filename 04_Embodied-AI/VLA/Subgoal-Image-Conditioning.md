---
title: Subgoal Image Conditioning
description: 将期望的近期视觉状态作为条件输入机器人策略，以提供比语言更丰富的任务规格
tags:
  - embodied-ai
  - vla
  - goal-conditioning
  - world-model
created: 2026-07-28
---

# Subgoal Image Conditioning

Subgoal Image Conditioning 是一种将**期望的近期视觉状态图像**作为策略条件输入的技术，用于补充语言指令无法表达的细节。

## Core Idea

语言指令（如“打开冰箱门”）可能缺少执行细节（如抓握把手的方式）。子目标图像直接展示任务完成后的场景外观，提供更具体的空间和对象状态信息。

## Multi-view Subgoals

通常使用多视角子目标：
- **基座相机视角**：环境/对象中心的结果
- **腕部相机视角**：手臂/夹爪的结果

这样可以同时指定场景变化和机器人自身姿态变化。

## Subgoal Generation

子目标图像可以来自：
- **真实未来帧**：训练时从轨迹中采样
- **World Model 生成**：测试时根据当前观察和指令生成

World Model 通常基于大规模图像生成/编辑模型初始化，并在大规模视频数据上微调。

## Benefits

- 改善语言跟随和空间定位
- 支持跨 embodiment 迁移（world model 可生成目标机器人视角的子目标）
- 将非机器人数据（人类视频、网络视频）的语义知识通过图像传递给策略

## Related Concepts

- [[Diverse-Prompting-for-VLA|Diverse Prompting for VL[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — 子目标图像是其多模态提示组件之一
- [[World-Model-for-Robotics|World Model for Robotic[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — 生成子目标图像的模型
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Actio[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — 接受子目标图像作为输入的机器人策略
- [[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]]|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — 常与子目标图像联合使用
- [[02_AI/Generative-Models/Classifier-Free-Guidance|Classifier-Free Guidanc[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — 可用于增强子目标条件控制

## 补充：来自 [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|subgoal-image-conditioning（已合并[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]]

### 生成子目标图像（π0.7 形式化）

子目标图像由一个轻量级世界模型 $g_\psi$ 生成：

$$
\max_{\psi} \mathbb{E}_{\mathcal{D}_g} \left[ \mathcal{L}_{\mathrm{CFM}} \left( \mathbf{g}_t^\star, g_\psi(\mathbf{o}_t, \hat{\ell}_t, m) \right) \right]
$$

- $\mathcal{L}_{\mathrm{CFM}}$ 为标准 conditional flow matching 损失
- $\mathbf{g}_t^\star = \mathbf{o}_{t_{\mathrm{end}}}$ 为片段末帧作为真实子目标
- $m$ 为 episode metadata

### 训练与应用

- 训练时以一定概率（如 25%）加入子目标图像
- 子目标图像可与子任务指令互相替换或互补
- 测试时异步生成子目标图像，VLA 使用最新可用的子目标

### 优缺点

- **优点**：提供语言难以描述的细粒度视觉信息；改善空间定位；增强语言跟随和泛化
- **局限**：需要额外世界模型；生成图像与真实图像之间存在分布偏移；增加推理复杂度

## Papers

- [[05_Papers/articles/pi0-7|π0.[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Promptin[[04_Embodied-AI/VLA/Episode-Metadata-Prompting|Episode Metadata Prompting]] — 使用 BAGEL 初始化的轻量 world model 生成多视角子目标图像
