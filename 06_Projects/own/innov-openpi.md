---
title: innov_openpi
description: 基于 OpenPI 框架的 VLA 训练与在线 RL 项目
tags: [project, vla, openpi, rl, flow-matching]
created: 2026-07-16
---

# innov_openpi

基于 OpenPI 框架的 VLA 机器人训练项目，包含 SFT 微调、RL Token 训练（Stage 1）、在线 RL 训练（Stage 2）以及 WebSocket 策略服务。

模型架构：π₀.₅ = PaliGemma 2B（视觉-语言编码）+ Gemma 300M（动作专家），通过 flow matching 生成动作。

## 技术栈

- π₀.₅、PyTorch
- Flow matching
- RL Token（Stage 1）
- TD3 + BC 在线 RL（Stage 2）
- WebSocket 策略服务

## 入口

- 代码：`/home/kemove/INNOV/projects/innov_openpi`
- 说明：`CLAUDE.md`、`README.md`

## 经验复盘

- [[08_Experiments/innov_openpi-normalization-spike|训练损失尖峰：quantile 归一化与低方差维度]]

## 关联

- [[06_Projects/own/innov-projects|INNOV-Projects]]
- [[06_Projects/external/openpi|openpi]]
- [[06_Projects/external/Evo-RLT|Evo-RLT]]
- [[06_Projects/own/robodeploy|robodeploy]]
