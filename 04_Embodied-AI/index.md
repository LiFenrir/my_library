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
  - [[04_Embodied-AI/VLA/VLA-Architecture|VLA Architecture]] — VLA 三阶段计算架构
  - [[04_Embodied-AI/VLA/Aerial-VLA|Aerial VLA]] — 面向空中平台的 VLA
  - [[04_Embodied-AI/VLA/Edge-VLA-Inference|Edge VLA Inference]] — 紧凑边缘 VLA 的 pre-fill 主导延迟分析
  - [[04_Embodied-AI/VLA/VLA-Edge-Characterization|VLA Edge Characterization]] — 大尺度 VLA 边缘瓶颈与 scaling 投影
  - [[04_Embodied-AI/VLA/Dual-Rate-VLA-Scheduling|Dual-Rate VLA Scheduling]] — 动作与语义双速率调度
  - [[03_Robotics/Control/Outer-Loop-Guidance|Outer-Loop Guidance]] — VLA 作为控制外环
  - [[02_AI/LLM/Knowledge-Preserving-Fine-Tuning|Knowledge-Preserving Fine-Tuning]] — 专业化训练与知识保持
  - [[06_Projects/external/lingbot/lingbot-vla|LingBot-VLA]]
  - [[06_Projects/external/lingbot/lingbot-vla-v2|LingBot-VLA-V2]]
- World-Model — 世界模型、视频预测、环境动力学
  - [[04_Embodied-AI/World-Model/World-Model|World Model]] — 世界模型总览（V-M-C 与 JEPA/H-JEPA 两条路线）
  - [[04_Embodied-AI/World-Model/Hierarchical-JEPA|Hierarchical JEPA]] — 分层联合嵌入预测架构
  - [[06_Projects/external/lingbot/lingbot-va|LingBot-VA]]
  - [[06_Projects/external/lingbot/lingbot-world-v2|LingBot-World-V2]]
- Robot-RL — 机器人强化学习、真实世界 RL
  - [[04_Embodied-AI/Robot-RL/index|Robot RL Index]] — 完整索引
  - [[04_Embodied-AI/Robot-RL/Offline-RL-for-VLA|Offline RL for VLA]] — VLA 离线 RL
  - [[04_Embodied-AI/Robot-RL/RECAP|RECAP]] — 重标注与策略提取
- Embodied-Brain — 具身大脑、认知架构、感知-动作统一（待填充）
- Sim2Real — 仿真到真实迁移、域随机化、真实世界适配（待填充）

## 相关项目

- [[06_Projects/external/lingbot/index|LingBot]] — 蚂蚁灵波科技具身智能仓库
- [[06_Projects/external/openpi|openpi]] — Physical Intelligence 官方 VLA 仓库
- [[06_Projects/external/wall-x|wall-x]] — WALL 系列开源 VLA 训练与推理栈
- [[06_Projects/external/lerobot|lerobot]] — Hugging Face 官方 PyTorch 机器人库

## 与相关目录的关系

- [[03_Robotics/index|03_Robotics]] — 机器人底层技术（感知、规划、控制、硬件、ROS2、工程）
- [[05_Papers/index|05_Papers]] — 论文精读与批注（VLA、World Model、Robot RL 等）
- [[06_Projects/index|06_Projects]] — 具体项目实践（如 lerobot、openpi、robodeploy）
- [[08_Experiments/index|08_Experiments]] — 实验记录与复盘

## 概念链

```
Concept → Theory → Paper → Engineering → Experiment → Project
```
