---
title: Catastrophic Forgetting
description: 神经网络在 sequential 或 specialized fine-tuning 过程中丢失已学知识的现象
tags:
  - ml
  - fundamentals
  - fine-tuning
  - continual-learning
  - knowledge-preservation
created: 2026-07-28
---

# Catastrophic Forgetting

Catastrophic Forgetting（灾难性遗忘）指模型在针对新任务或新领域进行 fine-tune 后，显著遗忘先前任务所学知识的现象。

## 典型场景

- 将通用视觉-语言模型 specialization 到机器人动作生成后，caption/VQA 能力下降。
- 将大语言模型微调为医疗/法律领域专家后，通用常识退化。
- 持续学习（continual learning）中按顺序学习多个任务时早期任务性能崩溃。

## 产生原因

- 新任务梯度大幅改变原本对旧任务重要的权重。
- 旧任务数据在 fine-tune 阶段不再出现，模型无法维持其决策边界。

## 常见缓解策略

| 策略 | 思路 |
|------|------|
| 数据回放（Data rehearsal） | fine-tune 时混入旧任务/通用数据 |
| 正则化方法 | 限制参数变化（如 EWC）或加蒸馏损失 |
| 知识蒸馏 | 让当前模型与旧模型输出保持一致 |
| 模块化/参数隔离 | 为不同任务分配独立子网络或 adapter |
| 多任务联合训练 | 同时优化新旧任务目标 |

## 与 VLA 的关联

在 dual-rate VLA 中，模型需要同时输出动作和语义解释。若仅使用动作数据 fine-tune，通用视觉-语言能力会严重退化，导致语义分支失效。混合目标与知识保持正则化是缓解该问题的关键。

## Related Concepts

- [[Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — VLA 场景下的具体实践
- [[01_Fundamentals/ML/index|ML Fundamentals]] — 机器学习基础
- [[02_AI/LLM/index|LLM]] — 大语言模型 fine-tuning

## Papers

- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 在 VLA 中观察到的 retention-reactivity tradeoff 示例
