---
title: "Recursive Multi-Agent System"
description: "多智能体在隐空间递归协作，通过系统级迭代优化提升复杂任务推理能力"
tags: [concept, ai, llm, multi-agent-system, latent-space]
created: 2026-07-30
---

# Recursive Multi-Agent System (RecursiveMAS)

**核心定义**：RecursiveMAS 是一种多智能体系统范式，多个异构智能体在**隐空间**中递归传递信息，通过系统级迭代优化协作解决复杂任务，而非一次性线性流水线。

## 为什么需要

单个大语言模型面临容量、短视生成和探索不足等瓶颈。传统多智能体系统多采用顺序流水线，每个智能体只处理一次输入并传递给下一个，缺乏跨智能体的深度迭代优化。

## 核心设计

### 1. 隐空间协作

不同于基于文本的多智能体通信，RecursiveMAS 在 Transformer 的连续隐状态空间中传递信息：

$$
h_{t+1}^{(i)} = f_{\theta_i}([E_{\leq t}; h_t^{(j)}; \dots])
$$

其中 $h_t^{(j)}$ 来自其他智能体的隐状态输出。

### 2. RecursiveLink 模块

轻量级两层残差投影模块，实现异构智能体间的隐状态传输：

- **Inner RecursiveLink**: 在每个智能体内部，对齐输入/输出空间的持续潜在思考
- **Outer RecursiveLink**: 桥接不同模型类型和规模的异构智能体的隐藏表示

相比文本通信，RecursiveLink 避免重复解码中间智能体输出，运行时效率更高。

### 3. 内外循环训练

- **内循环**: 训练各智能体的 Inner RecursiveLink，模型级预热
- **外循环**: 训练跨智能体的 Outer RecursiveLink，梯度通过完整递归轮次反向传播

潜在空间连接在训练期间保持稳定梯度流，避免文本交互引起的梯度消失。

### 4. 递归迭代

系统通过多轮递归让不同智能体反复修正和完善中间表示，形成集体推理轨迹。

### 3. 系统级训练

优化目标不仅提升单个智能体能力，还显式优化跨智能体协作，使整个系统性能超越单独微调每个智能体。

## 与文本通信多智能体的区别

| | 文本通信 MAS | 隐空间递归 MAS |
|---|---|---|
| 通信媒介 | 自然语言 | 连续隐状态 |
| 协作深度 | 单轮或浅层 | 多轮递归 |
| 信息密度 | 受限于文本 token | 可传递更丰富语义 |
| 训练目标 | 通常独立 | 系统级联合优化 |

## 优缺点

- **优点**：更强的协作深度、更高的信息密度、系统级优化；
- **缺点/局限**：训练复杂度高、智能体间隐状态对齐困难、可解释性较弱。

## 与其他概念的关系

- [[02_AI/LLM/Chain-of-Thought-Reasoning|Chain-of-Thought Reasoning]] — 单模型内部推理链
- [[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]]|[[02_AI/Cognitive-Architecture/Autonomous-Machine-Intelligence|Autonomous Machine Intelligence]] — 多模块认知架构
- [[02_AI/LLM/Mixture-of-Experts|Mixture of Experts]] — 异构专家协作的另一种形式

## 来源

- [[05_Papers/articles/recursive-multi-agent-systems|Recursive Multi-Agent Systems]]
