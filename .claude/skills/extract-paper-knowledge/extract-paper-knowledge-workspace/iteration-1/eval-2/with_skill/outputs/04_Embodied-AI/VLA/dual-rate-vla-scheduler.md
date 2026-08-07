---
title: "双速率 VLA 推理调度"
description: "在同一 VLA 上同时维持高频动作分支与低频语义分支的调度策略。"
tags: [concept, embodied-ai, vla, inference, scheduling]
created: 2026-07-28
---

# 双速率 VLA 推理调度

核心定义：让同一个 VLA 在同一硬件上按两个时间尺度运行：高频反应式动作输出与低频句子级语义输出。

## 原理

- 动作查询周期 $\Delta_a$ 与语义查询周期 $\Delta_s$ 满足整数倍关系：

$$
\Delta_s = K \Delta_a, \quad K \in \mathbb{N}, K > 1
$$

- 动作请求作为截止期关键路径立即执行；语义请求作为机会式后台任务，可被动作截止期抢占。
- 典型配置：动作约 20 Hz，语义约 6–7 Hz。

## 优缺点

- 优点：避免被慢速语义输出拖垮控制回路，同时保留场景理解与解释能力。
- 局限：需要显式调度器与资源隔离，动作与语义状态之间可能存在短暂不一致。

## 与其他概念的关系

- [[llm-vla-inference-latency|LLM/VLA 推理延迟分[[02_AI/AI-Infra/VLA-Inference|VLA Inference]] — 调度基于预填充主导的延迟特征。
- [[outer-loop-guidance|外环引[[02_AI/AI-Infra/VLA-Inference|VLA Inference]] — 动作分支输出外环引导指令。
- [[semantic-perception-service|语义感知作为低速服[[02_AI/AI-Infra/VLA-Inference|VLA Inference]] — 语义分支的角色定位。

## 来源

- [[05_Papers/articles/litevla-h|LiteVLA-[[02_AI/AI-Infra/VLA-Inference|VLA Inference]]
