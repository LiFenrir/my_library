---
title: "LingBot-VA"
description: "自回归视频-动作世界模型（AR diffusion），统一视觉动态预测与动作推理"
tags: [project, lingbot, embodied-ai, world-model, robot-learning]
created: 2026-07-28
source: "/home/kemove/INNOV/projects/lingbot/lingbot-va"
---

# LingBot-VA

自回归视频-动作世界模型（AR diffusion 框架），在单一交错序列中统一视觉动态预测与动作推理，用于机器人操作控制（仿真评测与真机部署）。

## 项目定位

- 架构：基于 Wan2.2 视频模型，双流 Mixture-of-Transformers（MoT），支持异步执行 + KV Cache 长时序推理
- 部署形态：独立运行（i2va 图生视频-动作）或 Server-Client 架构（WebSocket 服务，模型环境与仿真环境分离）
- 论文：arXiv:2601.21998《Causal World Modeling for Robot Control》
- 权重渠道：HuggingFace `robbyant/lingbot-va-*`，ModelScope `Robbyant/lingbot-va-*`
- 详细论文笔记：[[05_Papers/notes/causal-world-modeling|Causal World Modeling for Robot Control]]

## 目录结构

```text
lingbot-va/
├── wan_va/                        # 核心包
│   ├── wan_va_server.py           # 推理服务入口（VA_Server 类）
│   ├── train.py                   # 后训练入口（Trainer 类，FSDP）
│   ├── configs/                   # 各环境配置
│   ├── modules/
│   │   ├── model.py               # WanVATransformer3DModel 及注意力/KV Cache 实现
│   │   └── utils.py               # 模型加载
│   ├── dataset/
│   │   └── lerobot_latent_dataset.py  # LeRobot 格式 + VAE latent 数据集
│   ├── distributed/               # FSDP 封装与分布式初始化
│   └── utils/
│       ├── scheduler.py           # FlowMatchScheduler
│       ├── sever_utils.py         # 多 GPU 异步推理编排
│       └── Simple_Remote_Infer/deploy/  # WebSocket server/client 策略部署
├── script/                        # 启动脚本
├── evaluation/                    # RoboTwin / LIBERO 评测
├── example/                       # 示例数据
└── requirements.txt / pyproject.toml / INSTALL.md
```

## 核心类/函数/入口

| 符号 | 位置 | 职责 |
|---|---|---|
| `VA_Server` | `wan_va/wan_va_server.py` | 推理服务主类 |
| `VA_Server.infer(obs)` | 同上 | 服务端单步入口 |
| `VA_Server.generate()` | 同上 | i2va 独立模式 |
| `Trainer` | `wan_va/train.py` | 后训练主类：FSDP 分片、加噪、计算 latent+action 双流损失 |
| `WanVATransformer3DModel` | `wan_va/modules/model.py` | 核心 transformer：视频/动作双模态流，KV Cache |
| `WanAttention` | 同上 | 注意力层，`attn_mode ∈ {torch, flashattn, flex}` |
| `FlowMatchScheduler` | `wan_va/utils/scheduler.py` | Flow Matching 调度 |
| `MultiLatentLeRobotDataset` | `wan_va/dataset/lerobot_latent_dataset.py` | 多数据集聚合 |
| `run_async_server_mode` | `wan_va/utils/sever_utils.py` | 多 GPU 异步推理 + WebSocket 服务编排 |
| `VA_CONFIGS` | `wan_va/configs/__init__.py` | 配置注册表 |

## 输入/输出契约

### 服务端推理（`VA_Server.infer(obs)`）

- 输入 `obs`（dict，经 WebSocket + msgpack 传输）：
  - `reset: bool` — 为 True 时触发 `_reset(prompt)`，返回空 dict
  - `prompt: str` — 任务自然语言指令
  - `compute_kv_cache: bool` — 为 True 时仅预计算历史 KV Cache
  - `obs: list[dict[str, np.ndarray]]` — 历史观测帧，每帧含各相机图像 `(H, W, 3) uint8`
- 输出：`dict(action=np.ndarray)` — 动作形状 `(action_per_frame × frame_chunk_size, len(used_action_channel_ids))`

### 动作规范（数据集侧）

- 标准动作维度 `action_dim = 30`：左臂 EEF 7 + 右臂 EEF 7 + 左臂关节 7 + 右臂关节 7 + 左夹爪 1 + 右夹爪 1
- 归一化方式 `quantiles`（映射到 [-1, 1]），未使用通道由 `actions_mask` 屏蔽

## 依赖关系

- 与 lingbot 其他子项目：无代码级依赖，独立仓库
- 外部仿真环境：RoboTwin-2.0、LIBERO
- 基座模型：Wan2.2
- 数据格式：LeRobot v0.3.3
- 关键库：torch 2.9.0 + CUDA 12.6、diffusers 0.36.0、transformers 4.55.2、flash-attn、websockets、msgpack、lerobot 0.3.3、wandb
- Python 3.10.16

## 常用命令

```bash
# RoboTwin 评测
bash evaluation/robotwin/launch_server.sh
bash evaluation/robotwin/launch_client.sh <save_root> <task_name>

# LIBERO 评测
bash evaluation/libero/launch_server.sh
bash evaluation/libero/launch_client.sh

# 图生视频-动作（i2va 独立模式）
NGPU=1 CONFIG_NAME='robotwin_i2av' bash script/run_launch_va_server_sync.sh

# 后训练（FSDP 分布式）
NGPU=8 CONFIG_NAME='robotwin_train' bash script/run_va_posttrain.sh

# 格式化
make format
```

## 特殊约定

- `attn_mode` 必须手动修改：训练用 `"flex"`，推理用 `"torch"` 或 `"flashattn"`
- 推理开启 `enable_offload` 后 RoboTwin 约 24GB、i2av 约 18GB
- server 与 client 必须同机部署（RoboTwin 评测）
- 训练 checkpoint 保存为 diffusers 格式

## 相关链接

- 父项目：[[06_Projects/external/lingbot/index|LingBot]]
- 环境分析：[[06_Projects/external/lingbot/python-env-analysis|LingBot Python 环境差异分析]]
- 论文笔记：[[05_Papers/notes/causal-world-modeling|Causal World Modeling for Robot Control]]
