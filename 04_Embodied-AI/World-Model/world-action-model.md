---
title: "World Action Model (WAM)"
description: "联合建模视觉动力学预测与动作生成的世界模型变体"
tags: [concept, embodied-ai, world-model]
created: 2026-07-29
---

# World Action Model (WAM)

**核心定义**：World Action Model（WAM）是一类将视觉世界建模与动作生成统一在一个框架中的机器人策略模型。与标准 VLA 直接映射观测到动作不同，WAM 显式建模动作条件下的未来观测演化。

## 两种范式

1. **Imagine-then-Execute**：测试时先生成未来观测，再基于未来观测预测动作
2. **Train-only Video Modeling**：训练时使用视频预测目标学习表示，测试时跳过未来生成直接输出动作

## Fast-WAM 的核心发现

Fast-WAM 研究表明：WAM 的性能提升主要来自训练时的视频建模目标（帮助学习物理先验和动作条件表示），而非测试时的显式未来生成。移除测试时想象可使延迟降低 4 倍以上，同时保持竞争力。

## 与 VLA 的关系

- VLA：直接 $\pi(a|o)$，强调语义理解和多任务泛化
- WAM：显式 $p(o'|o,a)$ 或 $a \sim g(o,o')$，强调物理动力学和因果性

## 与其他概念的关系

- [[04_Embodied-AI/World-Model/World-Model|World Model]] — WAM 是世界模型在机器人控制中的具体化
- [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]]|Vision-Language-Action Model]] — 与 WAM 并行的策略范式
- [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — WAM 的一种因果实现

## 形式化表述

设当前观测为 $o$，语言指令为 $l$，未来动作为 $a_{1:H}$。标准视觉运动策略直接建模：
$$
p(a_{1:H} \mid o, l)
$$

WAM 引入未来视觉观测 $v_{1:T}$ 作为中间变量，常见的 imagine-then-execute 分解为：
$$
p(a_{1:H} \mid o, l) = \int p(v_{1:T} \mid o, l) \, p(a_{1:H} \mid o, l, v_{1:T}) \, dv_{1:T}
$$
即先预测未来观测，再基于未来观测生成动作。

Fast-WAM 则保留训练时的视频建模目标，但测试时不再显式生成 $v_{1:T}$，而是直接从当前上下文编码得到的隐式世界表示 $z(o,l)$ 输出动作：
$$
p_\theta(a_{1:H} \mid o, l) = p_\theta(a_{1:H} \mid z(o,l))
$$
其中 $z(o,l)$ 由视频主干单次前向传播获得。

## 代表性变体

- **Joint-modeling WAM**：未来视频 token 与动作 token 在同一模型中联合去噪
- **Causal / IDM WAM**：先生成未来视频，再将未来表示作为动作预测的条件
- **Fast-WAM**：训练时联合视频与动作流，推理时只保留第一帧干净 latent，经单次前向得到世界表示并直接解码动作

## 核心洞见

Fast-WAM 的对比实验显示：移除训练时视频协同训练（video co-training）会造成显著性能下降，而移除测试时显式未来生成仅带来小幅影响。这说明 WAM 的收益主要来自视频建模目标对表示学习的塑造，而非推理时的未来想象本身。

## DreamZero 与零样本泛化

DreamZero（World Action Models are Zero-shot Policies）将 WAM 训练于多样化机器人数据，实现跨任务、跨环境的零样本策略迁移：

- **联合视频-动作自回归建模**：同时预测未来观测 $o_{l:l+H}$ 与动作 $a_{l:l+H}$，等价于将 AR 视频预测与逆动力学模型结合；
- **自回归架构优于双向**：AR 推理利用 KV cache，速度快 $3\sim 4$ 倍，且动作更平滑；
- **数据多样性关键**：500h 遥操作数据覆盖 22 个真实环境，每个环境执行粗粒度任务而非重复单一技能

### DreamZero-Flash: 解耦噪声调度

标准训练共享视频和动作的噪声时间步，但少步推理需从高噪声视频预测干净动作。Flash 解法：

- 视频时间步偏向高噪声：$t_k^{\text{video}} = 1 - \eta, \quad \eta \sim \text{Beta}(7, 1)$
- 动作时间步保持均匀：$t_k^{\text{action}} \sim \mathcal{U}(0, 1)$
- 效果：扩散步数 4→1，推理延迟 350ms→150ms，性能仅降 9%

### 推理优化 (38× 加速)

| 层级 | 技术 | 加速 |
|------|------|------|
| 系统级 | CFG 并行（双 GPU）| 1.9× |
| | DiT Cache（速度方向一致性）| 5.5× |
| 实现级 | Torch Compile + CUDA Graphs | 8.9× |
| | NVFP4 量化 (GB200) | 16.6× |
| 模型级 | DreamZero-Flash | 38× |

最终达到 **7Hz 实时闭环控制**。

### 跨本体迁移

WAM 仅需 10-20 分钟视频数据（无动作标注）即可实现跨本体迁移：
- Human → Robot：+42% 任务进度
- Robot → Robot：+45% 任务进度
- 少样本新本体适应仅需 30 分钟数据

## WAM 缩放律

DreamZero 指出机器人基础模型中 WAM 的缩放律尚未充分探索：

- 模型规模、数据规模、训练算力对 WAM 能力的影响可能与 VLA 不同；
- WAM 由于显式建模未来观测，可能展现出更直接的动作能力缩放。

## 与其他概念的关系补充

- [[04_Embodied-AI/World-Model/privileged-foresight-distillation|Privileged Foresight Distillation]] — 另一种训练时利用未来信息的方法
- [[04_Embodied-AI/VLA/Flow-based-VLA|Flow-based VLA]] — DreamZero 使用流匹配训练 WAM

## 来源

- [[05_Papers/articles/fast-wam|Fast-WAM: Do World Action Models Need Test-time Future Imagination?]]
- [[05_Papers/articles/world-action-models-zero-shot|World Action Models are Zero-shot Policies]]
