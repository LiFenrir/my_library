---
title: Action Tokenization
description: 将连续机器人控制量离散化为语言模型可生成的 token，并在执行时反量化的技术。
tags:
  - embodied-ai
  - vla
  - action-representation
  - tokenization
  - concept
created: 2026-07-28
---

# Action Tokenization

Action Tokenization 是把**连续机器人控制量**（如线速度、角速度、关节位置）映射为语言模型词汇表中的离散 token，使 VLA 能用自回归方式生成动作。

## Why

VLA 的核心思想是把动作也当作“语言”来生成。为此需要把连续动作空间转换为离散 token 空间，从而复用 VLM 的 decoder。

## Core Idea

1. **编码**：将连续动作向量 `a ∈ R^d` 离散化为一个或多个 token id。
2. **生成**：VLA 模型自回归地预测动作 token 序列 `a_t = {a_1, ..., a_n}`。
3. **解码**：将生成的 token 反量化为连续控制量，发送给底层控制器。

## Methods

| 方法 | 说明 |
|------|------|
| 直接标量离散化 | 每个连续维度均匀分桶，映射为独立 token |
| 动作 chunking | 一次生成未来 K 步的动作序列 |
| 语义-动作混合 | 在统一序列中混合文本 token 与动作 token |

## In LiteVLA-Edge

- 模型输出短 action token 序列。
- 连续控制量（如 `v`, `ω`）从 token 反量化得到。
- 最终通过 ROS 2 发布为 `geometry_msgs/Twist`。

## Trade-offs

- **精度 vs. 词汇表**：桶越细，动作精度越高，但 vocab 越大、解码越慢。
- **延迟 vs. 平滑性**：单 token 输出延迟低；action chunking 输出平滑但增加首 token 延迟。
- **量化敏感性**：4-bit 量化后，动作 token 的数值稳定性需要验证。

## Related Concepts

- [[Vision-Language-Action|VLA]] — 动作 token 的应用范式
- [[LiteVLA-Edge|LiteVLA-Edge]] — 短 action token 输出案例
- [[GGUF-Quantization|GGUF Quantization]] — 量化对动作精度的影响

## Engineering

- 动作 token 设计需针对具体 embodiment 校准。
- 建议在仿真和真实环境中分别验证反量化后动作的平滑性与安全性。
- 对时间敏感任务，优先减少输出 token 数，或采用单 token action representation。

## Questions

- 是否可以为不同自由度学习联合 token 表示，而非独立标量？
- 动作 token 的分布是否与语言 token 冲突，需要特殊 embedding？
