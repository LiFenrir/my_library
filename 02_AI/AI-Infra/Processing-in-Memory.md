---
title: Processing-in-Memory
description: 将计算靠近存储阵列，以缓解内存墙瓶颈的架构范式
tags:
  - ai-infra
  - memory
  - computer-architecture
  - edge-inference
  - concept
created: 2026-07-30
---

# Processing-in-Memory (PIM)

Processing-in-Memory（PIM，存内计算/近存计算）把部分计算逻辑集成到存储器内部或靠近存储器的位置，减少数据在处理器与 DRAM 之间的搬运，从而缓解**内存墙（Memory Wall）**瓶颈。

## Why

传统冯·诺依曼架构中，数据需从 DRAM 搬移到处理器才能计算。对于访存密集的 workload：

- 数据搬运能耗远高于计算本身。
- 内存带宽成为性能上限，单纯提升算力收益有限。

在边缘 AI 推理（如 VLA 自回归解码）中，这一瓶颈尤为突出。

## Core Idea

```
传统：DRAM → 总线 → 处理器 → 写回 DRAM
PIM：   DRAM 内部或近旁完成计算 → 仅返回结果
```

关键收益：

- **带宽提升**：利用存储阵列内部高并行位线带宽。
- **能耗降低**：减少长距离数据搬移。
- **延迟改善**：对 memory-bound 算子可显著缩短执行时间。

## 典型实现形态

| 形态 | 说明 |
|------|------|
| 近存计算（Near-Memory Compute） | 计算单元靠近 DRAM，通过宽总线/3D 堆叠提升带宽 |
| 存内计算（In-Memory Compute） | 直接利用 DRAM 阵列的模拟/数字操作完成简单运算 |
| PIM-DRAM 商用方案 | 基于商用 DRAM 技术扩展指令集，如 LPDDR6X PIM |

## 在 AI 推理中的适用条件

PIM 最适合**运算强度低、访存主导**的阶段：

- 大模型自回归解码
- 稀疏/小 batch 推理
- 注意力中的某些访存密集算子

对计算密集、规则并行的前向层，传统加速器仍更优。

## Trade-offs

- **编程模型**：需显式划分适合 PIM 的算子，增加软件复杂度。
- **灵活性**：PIM 擅长固定模式计算，复杂控制流仍回退到主处理器。
- **精度与一致性**：存内模拟计算可能引入噪声，需校验数值正确性。

## Related Concepts

- [[Roofline-Model|Roofline Model]] — 判断 workload 是否 memory-bound 的工具
- [[VLA-Edge-Characterization|VLA Edge Characterization]] — PIM 作为边缘 VLA 潜在路径的分析实例
- [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘 VLA 的内存瓶颈来源
- [[AI-Edge-Performance-Evaluation|AI Edge Performance Evaluation]] — 评估 PIM 等未来硬件的模拟方法

## Papers

- [[05_Papers/articles/characterizing-vla-models|Characterizing VLA Models]] — 将 PIM 视为边缘 VLA 未来硬件路径之一
