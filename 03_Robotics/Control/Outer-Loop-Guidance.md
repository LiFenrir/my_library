---
title: Outer-Loop Guidance
description: 将 VLA 置于机器人/载具控制外环，由高频率底层控制器负责内环稳定的分层控制架构
tags:
  - robotics
  - control
  - vla
  - aerial-robotics
  - safety
created: 2026-07-28
---

# Outer-Loop Guidance

Outer-Loop Guidance 是一种分层控制设计：VLA 只负责生成**短周期的高层引导指令**，而传统的低层控制器继续以高频率执行姿态稳定、力控或电机控制。

## 核心思想

不要试图让 VLA 直接输出电机指令或高频率控制信号。相反：

- **VLA / 外环**：以较低但足够快的频率（如 ~20 Hz）输出动作 token，表示速度、航向、航点或模式指令。
- **底层控制器 / 内环**：以常规高频率（如 100–1000 Hz）维持姿态、高度、电机响应等稳定性。

## 为什么这样设计

1. **降低 VLA 的实时负担**：VLA 推理存在抖动，不适合直接驱动高带宽控制。
2. **安全隔离**： malformed 或 stale 的 action token 可被下游滤波器、限幅器和紧急停止逻辑拦截。
3. **保留现有控制器**：无需替换已经过验证的内环稳定器和安全监控。
4. **匹配 pre-fill dominant 的边缘推理**：短输出的 action token 可在紧凑截止时间内完成。

## 动作 token 的语义

在 aerial 场景中，action token 通常解释为：
- 速度或加速度指令
- 航向/偏航角变化
- 航点或目标模式
- 任务模式切换

而不是直接电机 PWM。

## 安全实践

- 拒绝过期的 action token。
- 将指令 clamp 到载具特定的安全包络。
- 在置信度下降或语义危险谓词触发时，回退到悬停、刹车、返航或经典避障。

## Related Concepts

- [[Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 外环动作分支与低速语义分支的调度
- [[Edge-VLA-Inference|Edge VLA Inference]] — 边缘 VLA 的延迟约束决定了外环可行的更新频率
- [[Aerial-VLA|Aerial VLA]] — 无人机等 aerial 平台对内外环分离的典型需求
- [[03_Robotics/Control/index|Control]] — 控制理论与底层控制器

## Papers

- [[05_Papers/articles/litevla-h|LiteVLA-H]] — 本笔记主要知识来源
