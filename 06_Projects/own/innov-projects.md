---
title: INNOV Projects
description: INNOV 机器人研究项目总览，沉淀各仓库定位与技术栈
tags: [project, robotics, vla, rl, lerobot, moc]
created: 2026-07-16
---

# INNOV Projects

`/home/kemove/INNOV/projects/` 下的代码仓库总览。按「自己搭建的项目」与「外部开源项目」粗分。

---

## 自己的项目

- [[06_Projects/own/innov-openpi|innov_openpi]] — 基于 OpenPI 的 π₀.₅ 训练流水线：SFT、RL Token（Stage 1）、在线 RL（Stage 2）。
- [[06_Projects/own/robodeploy|robodeploy]] — 基于 LeRobot 的真实机器人部署工具包，支持 S1/SO100/SO101/Koch/Aloha 等，集成 OpenPI WebSocket 策略推理。

---

## 外部开源项目

### 训练与算法

- [[06_Projects/external/Evo-RLT|Evo-RLT]] — SJTU-MINT 基于 LeRobot 0.5.1 的 [RLT](https://www.pi.website/research/rlt) 复现，覆盖 VLA 微调、RL Token、chunk actor-critic、真实机器人 rollout。
- [[06_Projects/external/RLinf|RLinf]] — 分布式 RL 框架，面向具身/推理/Agent，基于 Ray + Hydra，支持多节点 FSDP/Megatron 与 SGLang/vLLM rollout。
- [[06_Projects/external/wall-x|wall-x]] — WALL 系列开源 VLA 训练与推理栈，当前为基于 Qwen2.5-VL-3B 的 Wall-OSS-0.5。

### 基础库与官方实现

- [[06_Projects/external/lerobot|lerobot]] — Hugging Face PyTorch 机器人库，提供数据集、策略、训练/评估/控制工具。
- [[06_Projects/external/lerobot-0.3.2|lerobot-0.3.2]] — LeRobot 0.3.2 稳定版，含 SO-101/HopeJR/LeKiwi 教程与预训练模型。
- [[06_Projects/external/openpi|openpi]] — Physical Intelligence 官方 VLA 仓库，含 π₀ / π₀-FAST / π₀.₅ 基础检查点与示例。

---

## 入口选择

- VLA 训练/微调 → `innov_openpi` / `openpi` / `wall-x`
- RL Token / 在线 RL → `Evo-RLT` / `innov_openpi`
- 真实机器人采集/部署 → `robodeploy` / `lerobot`
- 大规模分布式 RL → `RLinf`

---

## 相关目录

- [[06_Projects/index|06_Projects]] — 项目总览
- [[04_Embodied-AI/index|04_Embodied-AI]] — 具身智能算法与模型
- [[03_Robotics/index|03_Robotics]] — 机器人底层技术
- [[05_Papers/index|05_Papers]] — 论文精读

> 本地路径：`/home/kemove/INNOV/projects/README.md`
