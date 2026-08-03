---
title: Coaching for VLAs
description: 通过人类逐步语言指令教授 VLA 执行新任务，并将辅导数据转化为自主高层策略的方法
tags:
  - embodied-ai
  - vla
  - human-robot-interaction
  - few-shot
created: 2026-07-28
---

# Coaching for VLAs

Coaching for VLAs 是一种通过**人类逐步语言指令**教授 VLA 新任务的方法，无需为每个新任务收集底层动作演示数据。

## Core Idea

对于复杂或全新的长程任务，直接给出高层语言指令可能不够。人类可以像教人一样，逐步提供子任务指令（如“拿起红薯”、“打开空气炸锅”），引导 VLA 完成整个任务。

## Pipeline

1. **人类辅导**：人类根据观察实时给出子任务指令，VLA 执行对应动作
2. **收集数据**：记录（观察、任务指令、子任务指令）序列
3. **训练高层策略**：用这些数据训练一个高层语言策略，自动输出子任务指令
4. **自主执行**：高层策略 + VLA 组合完成新任务

## Benefits

- 无需额外 teleoperation 数据
- 利用 VLA 强大的语言跟随能力
- 可将语言辅导快速转化为自主能力

## Requirements

- VLA 需具备良好的语言跟随和泛化能力
- 子任务指令需对应 VLA 已掌握或可泛化的技能

## Related Concepts

- [[04_Embodied-AI/VLA/Diverse-Prompting-for-VLA|Diverse Prompting for VLA]] — 子任务指令是 diverse prompting 的组成部分
- [[04_Embodied-AI/VLA/Compositional-Task-Generalization|Compositional Task Generalization]] — Coaching 是实现组合泛化的途径之一
- [[04_Embodied-AI/VLA/Vision-Language-Action-Model|Vision-Language-Action Model]] — 被辅导的对象

## Papers

- [[05_Papers/articles/pi0-7|π0.7]] — 通过 coaching 教授使用空气炸锅、烤面包机等新任务
