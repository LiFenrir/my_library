---
title: "Privileged Foresight Distillation"
description: "在训练时利用特权未来信息生成动作校正信号，推理时仅使用当前观测的 World Action Model 训练技术"
tags: [concept, embodied-ai, world-model, distillation, world-action-model]
created: 2026-07-30
---

# Privileged Foresight Distillation (PFD)

**核心定义**：Privileged Foresight Distillation 是一种训练时机制，让「能看到未来视频」的特权路径生成动作校正信号，再通过小适配器蒸馏到「仅使用当前观测」的快速推理路径。

## 核心问题

World Action Model（WAM）中，联合预测未来视频与动作在训练时有助于学习物理先验，但测试时生成未来视频代价高。研究发现测试时去掉未来生成仍能保持性能，这引发问题：

- 未来信息在训练中到底起什么作用？
- 直接去掉未来分支是否会丢失动作相关的未来内容？

## 两种解释

1. **正则化视角**：未来预测只是正则化，不携带动作专用的未来信息；
2. **校正视角**：未来信息包含动作相关的纠错信号，可被当前路径吸收。

PFD 采用并实现了第二种解释。

## 方法

### 训练阶段

- **特权路径**：以当前帧和未来帧为输入，输出动作；
- **当前路径**：仅以当前帧为输入，输出动作；
- **适配器**：当前路径的输出经过一个小适配器，拟合特权路径与当前路径之间的动作差异（校正信号）。

### 推理阶段

只实例化当前路径 + 适配器，不生成未来视频，保持低延迟。

## 形式化

设动作差异为：

$$
\Delta A = A_{\text{privileged}} - A_{\text{current}}
$$

适配器学习：

$$
\hat{\Delta A} = f_{\text{adapter}}(h_{\text{current}})
$$

最终动作为：

$$
A_{\text{final}} = A_{\text{current}} + \hat{\Delta A}
$$

## 优缺点

- **优点**：保留未来信息对动作的校正作用，同时推理速度接近纯当前路径策略；
- **缺点/局限**：需要训练时构造特权教师，增加了训练复杂度。

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/world-action-model|World Action Model]] — PFD 面向的模型范式
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 同样强调未来预测与动作生成的关系

## 来源

- [[05_Papers/articles/privileged-foresight-distillation|Privileged Foresight Distillation: Zero-Cost Future Correction for World Action Models]]
