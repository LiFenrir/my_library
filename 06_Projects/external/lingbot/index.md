---
title: "LingBot"
description: "蚂蚁灵波科技 lingbot 仓库五子项目汇总：VLA、世界模型、深度模型、视频-动作模型"
tags: [project, lingbot, embodied-ai, vla, world-model, depth, robot-learning]
created: 2026-07-28
source: "/home/kemove/INNOV/projects/lingbot"
---

# LingBot

蚂蚁灵波科技（Robbyant）开源的具身智能仓库，包含多个面向机器人学习与控制的子项目。

## 子项目

| 子项目 | 定位 | 负责 Agent | 权重渠道 |
|---|---|---|---|
| [[06_Projects/external/lingbot/lingbot-depth|lingbot-depth]] | 基于 Masked Depth Modeling 的空间感知基础模型 | lingbot-depth-agent | HF/ModelScope `robbyant/lingbot-depth-*` |
| [[06_Projects/external/lingbot/lingbot-va|lingbot-va]] | 自回归视频-动作世界模型（AR diffusion） | lingbot-va-agent | HF/ModelScope `robbyant/lingbot-va-*` |
| [[06_Projects/external/lingbot/lingbot-vla|lingbot-vla]] | 4B VLA 基础模型（Qwen2.5-VL + 动作专家） | lingbot-vla-agent | HF/ModelScope `robbyant/lingbot-vla-*` |
| [[06_Projects/external/lingbot/lingbot-vla-v2|lingbot-vla-v2]] | 第二代 VLA（Qwen3-VL + MoE 动作专家） | lingbot-vla-v2-agent | HF/ModelScope `robbyant/lingbot-vla-v2-6b` |
| [[06_Projects/external/lingbot/lingbot-world-v2|lingbot-world-v2]] | 可交互视频世界模型（Wan2.2 因果扩散） | lingbot-world-v2-agent | HF/ModelScope `robbyant/lingbot-world-v2-14b-causal-fast` |

## 核心入口速查

### lingbot-depth
- `mdm/model/v2.py:MDMModel.infer` — 推理唯一入口
- `example.py` — CLI 推理示例

### lingbot-va
- `wan_va/wan_va_server.py:VA_Server.infer` — 服务端推理
- `wan_va/train.py:Trainer` — FSDP 后训练
- `evaluation/robotwin/`、`evaluation/libero/` — 评测

### lingbot-vla
- `tasks/vla/train_lingbotvla.py:main` — 训练入口
- `deploy/lingbot_vla_policy.py` — 推理/WebSocket 部署
- `lingbotvla/models/vla/pi0/modeling_lingbot_vla.py:LingbotVlaPolicy` — 主模型

### lingbot-vla-v2
- `tasks/vla/train_lingbotvla.py:main` — 训练入口
- `deploy/lingbot_vla_v2_policy.py` — 推理/WebSocket 部署
- `lingbotvla/models/vla/lingbot_vla/modeling_lingbot_vla_v2.py:LingbotVlaV2Policy` — 主模型

### lingbot-world-v2
- `generate.py` — 唯一推理 CLI
- `wan/image2video.py:WanI2VCausal.generate` — 推理流水线

## 环境分组

**不能共用一个环境**，核心冲突：PyTorch 版本（2.6.0 / 2.8.0 / 2.9.0）、transformers 区间互斥、lerobot 版本分裂。

| 环境 | 项目 | 关键版本 |
|---|---|---|
| env-A：vla 系 | lingbot-vla + lingbot-vla-v2 | Python 3.12 + torch 2.8.0 (cu128) + flash-attn 2.8.3 + lerobot 0.4.2 |
| env-B：va | lingbot-va | Python 3.10 + torch 2.9.0 (cu126) + transformers 4.55.2 + lerobot 0.3.3 |
| env-C：depth | lingbot-depth | Python 3.9+ + torch 2.6.0 + xformers 0.0.29.post2 |
| env-D：world-v2 | lingbot-world-v2 | Python 3.10+ + torch>=2.4 + transformers<=4.51.3 |

详细分析见 [[06_Projects/external/lingbot/python-env-analysis|LingBot Python 环境差异分析]]。

## 子项目依赖关系

```text
lingbot-depth
    ├─ 被 lingbot-vla 以 git 子模块引入（深度蒸馏版）
    └─ 被 lingbot-vla-v2 以 vendored 形式内嵌（MoRGBD 几何教师）

lingbot-vla ──┐
lingbot-vla-v2 ├─ 共享 torch 2.8 / flash-attn 2.8.3 / lerobot 0.4.2 底座
lingbot-va     │
lingbot-world-v2 ─ 独立，无代码级依赖
```

## 关键约定

- 全 workspace 统一：导入必须在文件顶部，禁止函数内联导入；注释用中文、1-2 行，只写核心功能与 API 契约。
- 跨项目改动须经 LingBot-Lead 协调，各子项目由对应 Agent 负责执行。

## 相关链接

- 项目仓库：`/home/kemove/INNOV/projects/lingbot`
- 论文：
  - [[05_Papers/notes/causal-world-modeling|Causal World Modeling for Robot Control]]（lingbot-va）
  - [[05_Papers/articles/causal-world-modeling|Causal World Modeling 原文]]
