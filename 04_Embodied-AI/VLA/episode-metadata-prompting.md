---
title: "Episode Metadata Prompting"
description: "将 episode 级别属性（速度、质量、是否犯错）作为提示注入 VLA 以解歧数据分布"
tags: [concept, embodied-ai, vla, prompting]
created: 2026-07-29
---

# Episode Metadata Prompting

**核心定义**：Episode Metadata Prompting 是向 VLA 的上下文提示中添加描述训练 episode 属性的元数据（如速度、质量、是否犯错），使模型能够区分不同质量的数据并在测试时被引导到期望行为。

## 原理

当训练数据包含多样化、甚至次优的 episode 时，模型可能会对这些模式取平均，导致性能次优。通过显式标注 episode 属性，模型可以：

- 正确理解每个样本的行为质量
- 学习将 metadata 与目标动作关联
- 在测试时通过 metadata 提示指定期望行为

## 常见元数据

| 属性 | 含义 | 示例 |
|------|------|------|
| Overall speed | episode 长度（步数） | "8000 steps" |
| Overall quality | 执行质量评分 1-5 | "Quality: 5" |
| Mistake | 该片段是否包含错误 | "Mistake: false" |

## 与 CFG 结合

π0.7 在推理时使用 [[02_AI/Classifier-Free-Guidance|Classifier-Free Guidance]] 对 metadata 进行增强：

$$
\nabla_{\mathbf{a}} \log \pi_\theta(\mathbf{a} | \mathbf{o}, \mathcal{C}) + \beta \left( \nabla_{\mathbf{a}} \log \pi_\theta(\mathbf{a} | \mathbf{o}, \mathcal{C}) - \nabla_{\mathbf{a}} \log \pi_\theta(\mathbf{a} | \mathbf{o}, \mathcal{C}^{\text{uncond}}) \right)
$$

通过设置高 quality、高 speed、无 mistake 的 metadata，可以引导模型产生更快、更高质量的动作。

## 训练时的 Dropout

- 训练时随机 dropout 各 prompt 组件，使模型能在测试时灵活组合
- metadata 整体 dropout 15%，各组件单独 dropout 5%

## 优缺点

- **优点**：有效利用次优和失败数据；测试时可 steer 模型行为；无需为每种行为单独收集数据
- **缺点/局限**：需要额外标注；metadata 设计依赖任务领域知识；错误标注会误导模型

## 与其他概念的关系

- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — metadata 是 VLA 上下文的一部分
- [[02_AI/Classifier-Free-Guidance|Classifier-Free Guidance]] — 常与 metadata prompting 联合使用
- [[04_Embodied-AI/VLA/Subgoal-Image-Conditioning|Subgoal Image Conditioning]] — 与 metadata 同属多模态上下文条件

## 来源

- [[05_Papers/articles/pi0-7|π0.7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities]]，第 V-C、VII 节
