---
title: "利用 episode metadata 学习混合质量数据"
description: "通过速度、质量、错误等元数据区分数据模式，使 VLA 在扩大数据集时持续提升。"
tags: [embodied-ai, vla, data-centric, episode-metadata, scaling]
created: 2026-07-28
---

# 利用 episode metadata 学习混合质量数据

真实机器人数据集往往包含演示、失败、次优自主 rollouts 和 RL 训练数据。直接混合训练容易让模型学到平均行为而退化。

## 问题

- 同一任务存在多种速度/质量/策略模式。
- 不加区分时，模型会趋向“平均”，导致动作模糊、性能下降。

## 解决思路

为每个训练片段附加 **episode metadata**：

- **Overall speed**：episode 长度分桶，代表快慢模式。
- **Overall quality**：人工标注的 1–5 分质量。
- **Mistake**：该片段是否包含错误。

模型通过条件 $p(\mathbf{a} \mid \mathbf{o}, \text{metadata})$ 学习把 metadata 与对应行为关联。

## 训练与测试

- 训练时 metadata 以一定概率 dropout，保证测试时灵活使用。
- 测试时固定使用高质量模式：quality=5、mistake=false、speed 取任务较快的 15th 百分位。
- 可使用 CFG 进一步增强高质量模式。

## 实验结论

- 有 metadata 时，增加数据量（即使平均质量下降）仍能持续提升性能。
- 无 metadata 时，引入低质量数据反而可能损害性能。
- 允许把 RL 训练 specialist 的 rollouts 蒸馏进通用模型，同时保留通用性。

相关：
- [[04_Embodied-AI/VLA/multimodal-context-conditioning|VLA 的多模态上下文条件]] — metadata 在 prompt 中的定义
- [[04_Embodied-AI/VLA/VLA-architecture|VLA 架构要素]]
- [[05_Papers/articles/pi0-7|pi0.7 论文笔记]]
