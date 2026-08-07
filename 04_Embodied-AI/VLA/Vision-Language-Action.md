---
title: Vision-Language-Action
description: 将视觉感知、语言理解与机器人动作生成统一在单一模型中的具身智能范式
aliases:
  - Vision-Language-Action Model
tags:
  - embodied-ai
  - vla
  - robotics
  - concept
  - foundation-model
created: 2026-07-28
---

# Vision-Language-Action (VLA)

VLA 是将**视觉感知、自然语言条件、机器人动作生成**统一在单一多模态模型中的策略范式。它直接根据视觉观测和语言指令生成机器人低层控制信号，是具身智能的基础模型路线之一。

## Why

传统机器人 pipeline 把感知、理解、规划、控制拆成独立模块，接口脆弱且难以利用互联网规模的视觉-语言先验。VLA 通过把动作也表示成语言模型的 token（或动作专家输出），让预训练 VLM 直接输出可执行动作。

## 条件生成视角

把机器人控制问题建模为条件语言建模：

```
P(a_t | I_t, g; θ)
```

- `I_t`：当前视觉观测
- `g`：自然语言目标/指令
- `a_t`：动作序列（离散 token 或连续动作）

模型在一个端到端目标下同时学习视觉 grounding、语义理解和动作生成。

## 典型架构（π0.7 形式化）

- **VLM Backbone**：处理视觉和语言输入，提供多模态表示
- **Observation Encoder**：将相机图像和本体感受编码为 token
- **Action Head / Action Expert**：基于 VLM 表示生成动作，常用 [[02_AI/Generative-Models/Flow-Matching|Flow Matching]] 或 [[01_Fundamentals/ML/diffusion-model|Diffusion]] 建模多峰动作分布
- **动作块预测**：基于近期观测历史预测未来动作序列，执行时只使用前几步（见 [[04_Embodied-AI/VLA/Action-Chunking|Action Chunking]]）

训练目标通常最大化动作序列的对数似然：

$$
\max_\theta \mathbb{E}_{\mathcal{D}} \left[ \log \pi_\theta(a_{t:t+H} \mid o_{t-T:t}, \mathcal{C}_t) \right]
$$

## 关键挑战

- 动作多模态性：同一指令可对应多种执行方式
- 跨 embodiment 泛化：不同机器人形态共享策略
- 长程任务与实时推理的平衡
- 表示纠缠：单一网络同时学习视觉理解、物理动力学和运动控制（可用世界模型缓解）

## 优缺点

- **优点**：可直接利用预训练 VLM 的视觉-语言理解能力；语言/视觉上下文提供灵活的任务指定方式
- **局限**：本质上是条件模仿学习，对数据分布敏感；推理延迟和动作块长度需要权衡

## Related Concepts

- [[02_AI/VLM/Vision-Language-Model|Vision-Language Model]] — VLA 的感知与语言 backbone
- [[04_Embodied-AI/VLA/Action-Expert|Action Expert]] — 负责动作生成的子模块
- [[04_Embodied-AI/VLA/Action-Tokenization|Action Tokenization]] — 连续动作如何离散化为 token
- [[04_Embodied-AI/VLA/Action-Chunking|Action Chunking]] — 动作块预测与执行
- [[04_Embodied-AI/VLA/Flow-based-VLA|Flow-based VLA]] — 使用流匹配动作生成的 VLA
- [[04_Embodied-AI/VLA/Diverse-Prompting-for-VLA|Diverse Prompting for VLA]] — 通过丰富提示增强 VLA 能力
- [[04_Embodied-AI/VLA/Cross-embodiment-Generalization|Cross-embodiment Generalization]] — VLA 的跨机器人泛化
- [[04_Embodied-AI/VLA/Knowledge-Insulation|Knowledge Insulation]] — VLM 与动作专家的知识隔离
- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — 与 VLA 并行的机器人策略范式
- [[01_Fundamentals/ML/Imitation-Learning|Imitation Learning]] — VLA 训练通常属于大规模条件行为克隆
- [[Edge-VLA|Edge VLA]] / [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘部署

## Papers

- [[05_Papers/notes/pi0-7|π0.7]] — 通过多样化提示实现可引导的通用 VLA
- [[05_Papers/notes/pi-0-6|π0.6]] — 早期流匹配 VLA
- [[05_Papers/notes/openvla|OpenVLA]] — 开源通用 VLA
- [[05_Papers/notes/rt-2|RT-2]] — 将 web 知识迁移到机器人控制
- [[05_Papers/notes/litevla-edge|LiteVLA-Edge]] — Jetson Orin 上的量化本地 VLA
- [[05_Papers/notes/litevla-h|LiteVLA-H]] — 双速率边缘 VLA 调度

## Engineering

- 动作 token 设计直接影响控制精度与延迟
- 模型规模、量化精度、推理运行时共同决定边缘部署可行性
- ROS 2 等中间件常用于把 VLA 输出桥接到真实执行器

## Questions

- 动作 token 空间如何平衡表达力与解码效率？
- 大模型通用性 vs. 小模型实时性如何权衡？
- 多模态 pre-fill 成本是边缘 VLA 的主要瓶颈吗？
