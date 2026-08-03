---
title: Mixture-of-Transformers
description: 在 Transformer 块级别为不同模态保留独立参数空间，同时通过跨模态注意力实现融合
tags:
  - architecture
  - multimodal
  - transformer
  - mot
  - ai
created: 2026-07-28
---

# Mixture-of-Transformers

**Mixture-of-Transformers（MoT）** 是一种多模态 Transformer 架构：不同模态拥有独立的 Transformer 块与参数空间，层间通过跨模态注意力相互条件，既避免模态干扰又保留融合能力。

## Core Idea

与在所有模态上共享同一 Transformer 不同，MoT 为每种模态维护独立的 QKV 投影与自注意力计算，再通过 cross-modal attention 让模态间交换信息。

## Architecture

典型双路 MoT 结构：

1. **独立 Transformer 块**：视频流与动作流分别计算自己的 query/key/value；
2. **维度对齐**：将低维模态 token 投影到高维模态空间参与联合自注意力；
3. **残差回投影**：联合注意力结果通过残差连接映射回原维度，保留模态专属表示；
4. **输出头**：各模态使用自己的解码头（如动作线性投影头）。

## Why It Works

- **避免表示纠缠**：视觉数据分布复杂、动作分布相对简单，独立参数防止简单动作信号被视觉特征淹没；
- **非对称容量**：可为不同模态配置不同宽度/深度（如视频流大、动作流小）；
- **灵活初始化**：动作流可用视频流预训练权重插值初始化并缩放方差，稳定联合训练。

## In Robotics

MoT 常用于统一视频-动作序列建模：
- 视频 token 与动作 token 按时间交错成单一序列；
- 视频流负责预测未来视觉状态；
- 动作流负责基于预测状态解码控制指令；
- 两者通过 MoT 层相互条件，实现"想象"与"执行"的耦合。

## 补充：来自 [[02_AI/LLM/Mixture-of-Transformers|mixture-of-transformers（已合并）]]

### 与 MoE 的关系

- MoE（Mixture-of-Experts）通常在 FFN 层做 token 级路由
- MoT 更强调整个 Transformer 层/块作为专家，分别负责不同模态或目标

### Motus 的三专家实例

Motus 用三个专家：理解专家（understanding）、视频生成专家（video generation）、动作专家（action），通过 UniDiffuser 风格的调度器灵活切换建模模式。详见 [[05_Papers/articles/motus|Motus: A Unified Latent Action World Model]]。

## Related Concepts

- [[Mixture-of-Experts]] — 在专家子网络级别稀疏扩展容量的相关架构
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 使用 MoT 统一视频-动作自回归建模的机器人世界模型
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 多模态输入输出策略
- [[02_AI/VLM/Cross-Modal-Attention|Cross-Modal Attention]] — 跨模态注意力机制

## Papers

- [[05_Papers/articles/causal-world-modeling|Causal World Modeling for Robot Control]] — LingBot-VA 采用非对称双路 MoT 架构
