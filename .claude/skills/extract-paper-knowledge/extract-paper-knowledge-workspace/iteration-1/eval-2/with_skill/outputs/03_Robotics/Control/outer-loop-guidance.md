---
title: "外环引导与内环稳定分离"
description: "将高层策略输出的动作指令作为外环引导，由传统飞控或低层控制器负责高频内环稳定。"
tags: [concept, robotics, control, guidance, vla]
created: 2026-07-28
---

# 外环引导与内环稳定分离

核心定义：将 VLA 输出的动作 token 解释为速度、航向、航点或模式级的外环引导命令，而不是直接电机指令。

## 原理

- 外环（outer loop）：由 VLA 以较低频率生成目标指令，负责任务级决策。
- 内环（inner loop）：由传统控制器以高频率执行姿态/电机稳定，负责动力学响应。
- 中间加入命令校验、限幅与紧急停止逻辑，降低 VLA 时延抖动带来的安全风险。

## 优缺点

- 优点：安全边界清晰、可复用成熟控制器、VLA 延迟对系统影响可控。
- 局限：需要额外接口与状态机设计，动作空间受外环抽象限制。

## 与其他概念的关系

- [[vision-language-action|VLA]] — 外环策略可由 VLA 担任。
- [[dual-rate-vla-scheduler|双速率 VLA 调度]] — 外环更新频率由调度器决定。

## 来源

- [[05_Papers/articles/litevla-h|LiteVLA-H]]
