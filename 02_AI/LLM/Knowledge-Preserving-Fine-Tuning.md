---
title: Knowledge-Preserving Fine-Tuning
description: 在将通用多模态模型专业化到具体任务时，通过混合目标与蒸馏正则化缓解灾难性遗忘
tags:
  - llm
  - fine-tuning
  - vla
  - catastrophic-forgetting
  - distillation
created: 2026-07-28
---

# Knowledge-Preserving Fine-Tuning

当把通用视觉-语言模型（VLM/VLA）fine-tune 到具体任务（如机器人动作生成、无人机导航）时，容易在提升任务性能的同时**丢失通用的视觉-语言能力**。Knowledge-Preserving Fine-Tuning（KP-FT）通过混合训练目标来缓解这一问题。

## 混合损失

总目标可写成：

```
L = λ_a · L_act + λ_s · L_sem + λ_g · L_gen + λ_kp · L_kp
```

- `L_act`：动作任务损失（如行为克隆）
- `L_sem`：领域语义损失（如 aerial 场景描述）
- `L_gen`：通用 caption / VQA 损失
- `L_kp`：知识保持正则项（可选）

典型权重示例（来自 LiteVLA-H）：
- λ_a = 1.0
- λ_s = 0.5
- λ_g = 0.2
- λ_kp = 0.1

## 知识保持正则项

一种实用选择是：在保留的通用多模态数据流上，对当前模型与预专业化 backbone 的输出做 KL 散度蒸馏。

```
L_kp = KL(p_θ0(·|I, x) || p_θ(·|I, x))
```

其中 θ0 是 specialization 前的原始模型参数。

## 保留-反应性权衡

- **仅动作数据 fine-tune**：动作成功率最高，但通用 caption 能力严重退化（灾难性遗忘）。
- **加入领域语义数据**：恢复 domain awareness。
- **加入通用 caption/VQA rehearsal**：进一步恢复通用能力。
- **完整 KP-FT**：在动作成功率与保留能力之间取得平衡。

## 工程价值

对于需要**既要做动作、又要能解释**的系统（如 dual-rate VLA），KP-FT 是避免模型退化为狭窄动作分类器的关键。

## 补充：来自 [[02_AI/LLM/Knowledge-Preserving-Fine-Tuning|knowledge-preserving-fine-tuning（已合并）]]

### 为什么需要

- 仅微调动作数据会导致严重的灾难性遗忘
- 通用能力（captioning、VQA）对机器人系统的可解释性和安全性仍然重要
- 混合数据可以在任务性能和通用能力之间取得平衡

### 优缺点

- **优点**：减少灾难性遗忘；保持模型多面性；提高部署安全性
- **局限**：需要更多训练数据；混合权重需要 tune；可能轻微牺牲任务性能

### 相关基础概念

- [[02_AI/LLM/Fine-Tuning|Fine-Tuning]] — 通用微调方法
- [[02_AI/LLM/Continual-Learning|Continual Learning]] — 知识保持是持续学习的核心问题

## Related Concepts

- [[04_Embodied-AI/VLA/Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 需要模型同时保留动作与语义能力
- [[04_Embodied-AI/VLA/Edge-VLA-Inference|Edge VLA Inference]] — 紧凑模型专业化的边缘推理场景
- [[01_Fundamentals/ML/Catastrophic-Forgetting|Catastrophic Forgetting]] — 通用概念
- [[02_AI/LLM/index|LLM]] — 大语言模型 fine-tuning 基础

## Related Entries

- 主归属：[[02_AI/LLM/index|LLM]]
- 在 VLA 中的角色：[[04_Embodied-AI/VLA/index|VLA]]

## Papers

- [[05_Papers/notes/litevla-h|LiteVLA-H]] — 本笔记主要知识来源
