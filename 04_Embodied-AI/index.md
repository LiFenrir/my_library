---
title: "04_Embodied-AI"
description: "具身智能知识库：VLA、World Model、机器人强化学习、具身大脑、Sim2Real。"
tags: [moc, embodied-ai, vla, world-model, robot-rl]
created: 2026-07-22
---

# 04_Embodied-AI

具身智能（Embodied AI）知识资产：让 AI 通过物理或仿真身体与世界交互的方法、模型与系统。

通用 AI（LLM、Agent 等）请移步 [[02_AI/index|02_AI]]。

## 子领域

- VLA — Vision-Language-Action 模型、机器人策略
  - [[04_Embodied-AI/VLA/index|VLA Index]] — 完整索引
  - [[04_Embodied-AI/VLA/Vision-Language-Action|Vision-Language-Action]] — VLA 通用定义
  - [[04_Embodied-AI/VLA/VLA-Architecture|VLA Architecture]] — 三阶段计算架构
  - [[04_Embodied-AI/VLA/Edge-VLA|Edge VLA]] — 面向嵌入式平台的轻量 VLA
  - [[04_Embodied-AI/VLA/Edge-VLA-Inference|Edge VLA Inference]] — 边缘 VLA 的延迟特征
- World-Model — 世界模型、视频预测、环境动力学
  - [[04_Embodied-AI/World-Model/index|World Model Index]] — 完整索引
  - [[04_Embodied-AI/World-Model/World-Model|World Model]] — 总览
  - [[04_Embodied-AI/World-Model/Hierarchical-JEPA|Hierarchical JEPA]] — 分层联合嵌入预测架构
  - [[04_Embodied-AI/World-Model/causal-world-model|Causal World Model]] — 因果世界模型
- Robot-RL — 机器人强化学习、真实世界 RL
  - [[04_Embodied-AI/Robot-RL/index|Robot RL Index]] — 完整索引
  - [[04_Embodied-AI/Robot-RL/Offline-RL-for-VLA|Offline RL for VLA]] — VLA 离线 RL
  - [[04_Embodied-AI/Robot-RL/RECAP|RECAP]] — 重标注与策略提取
  - [[04_Embodied-AI/Robot-RL/Long-Horizon-Manipulation-Reward|Long-Horizon Manipulation Reward]] — 长程操作奖励设计
- Robot-Planning — 机器人任务与运动规划
  - [[04_Embodied-AI/Robot-Planning/index|Robot Planning Index]] — 完整索引
  - [[04_Embodied-AI/Robot-Planning/Hierarchical-Planning|Hierarchical Planning]] — 分层任务分解
- Sim2Real — 仿真到真实迁移、域随机化、真实世界适配
  - [[04_Embodied-AI/Sim2Real/index|Sim2Real Index]] — 完整索引
  - [[04_Embodied-AI/Sim2Real/Domain-Randomization|Domain Randomization]] — 域随机化
  - [[04_Embodied-AI/Sim2Real/human-to-robot-data-augmentation|Human-to-Robot Data Augmentation]] — 人体视频数据增强
- [[04_Embodied-AI/Data-and-Evaluation/index|Data and Evaluation]] — 数据合成、动作表示与评估
  - [[04_Embodied-AI/Data-and-Evaluation/Ego-to-Robot-Synthesis|Ego-to-Robot Synthesis]] — 从人体视频合成机器人训练数据
  - [[04_Embodied-AI/Data-and-Evaluation/Camera-Frame-Relative-EEF|Camera-Frame Relative EEF]] — 相机坐标系相对 EEF 动作表示
  - [[03_Robotics/Simulation/Disentangled-Robot-Generalization-Benchmark|Disentangled Generalization Benchmark]] — 解耦泛化评估
- Embodied-Brain — 具身大脑、认知架构、感知-动作统一（待填充）

## 相关项目

- [[06_Projects/external/lingbot/index|LingBot]] — 蚂蚁灵波科技具身智能仓库
- [[06_Projects/external/openpi|openpi]] — Physical Intelligence 官方 VLA 仓库
- [[06_Projects/external/wall-x|wall-x]] — WALL 系列开源 VLA 训练与推理栈
- [[06_Projects/external/lerobot|lerobot]] — Hugging Face 官方 PyTorch 机器人库

## 与相关目录的关系

- [[03_Robotics/index|03_Robotics]] — 机器人底层技术（感知、规划、控制、硬件、ROS2、工程）
- [[05_Papers/index|05_Papers]] — 论文精读与批注
- [[06_Projects/index|06_Projects]] — 具体项目实践
- [[08_Experiments/index|08_Experiments]] — 实验记录与复盘

## 概念链

```
Concept → Theory → Paper → Engineering → Experiment → Project
```
