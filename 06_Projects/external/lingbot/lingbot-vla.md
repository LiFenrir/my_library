---
title: "LingBot-VLA"
description: "4B 参数 Vision-Language-Action 基础模型，基于 Qwen2.5-VL + Qwen2 动作专家"
tags: [project, lingbot, embodied-ai, vla, robot-learning]
created: 2026-07-28
source: "/home/kemove/INNOV/projects/lingbot/lingbot-vla"
---

# LingBot-VLA

4B 参数的 Vision-Language-Action（VLA）基础模型：以 Qwen2.5-VL-3B 为 VLM 基座、外挂 Qwen2 动作专家（action expert），通过 flow matching 从噪声中采样动作 chunk；基于 2 万小时真实双臂机器人数据预训练，提供无深度版与深度蒸馏版两套权重。

## 项目定位

- 仓库路径：`/home/kemove/INNOV/projects/lingbot/lingbot-vla/`
- 预训练数据：约 2 万小时真实双臂机器人数据
- 部署：通过 WebSocket 服务部署到仿真（RoboTwin/LIBERO）与真实机器人
- 权重渠道：HuggingFace / ModelScope `robbyant/lingbot-vla-*`

## 目录结构

```text
lingbot-vla/
├── train.sh                    # torchrun 启动包装
├── install.sh                  # 安装脚本
├── setup.py / pyproject.toml
├── tasks/vla/train_lingbotvla.py  # 训练唯一入口
├── deploy/                     # 推理/WebSocket 部署
├── lingbotvla/                 # 核心 Python 包
│   ├── models/                 # 模型构建/加载/注册 + VLA 主模型
│   ├── data/                   # 数据集、collator、动态 batching
│   ├── distributed/            # FSDP2 / 序列并行 / offloading
│   ├── checkpoint/             # dcp 检查点
│   ├── ops/                    # attention、MoE、loss 算子
│   ├── optim/                  # 优化器与调度
│   └── utils/                  # 参数、日志、helper
├── configs/                    # 训练配置 + 机器人特征映射
├── scripts/                    # 下载、评估、格式转换
└── experiment/                 # 实验说明
```

## 核心类/函数/入口

| 符号 | 位置 | 职责 |
|------|------|------|
| `main` | `tasks/vla/train_lingbotvla.py:59` | **训练唯一入口** |
| `LingbotVlaPolicy` | `lingbotvla/models/vla/pi0/modeling_lingbot_vla.py:1373` | 策略主类 |
| `FlowMatching.sample_actions` | 同上 | **动作采样核心** |
| `QwenvlWithExpertModel` | 同上 | VLM 与动作专家双流前向 |
| `LingbotVLAServer` | `deploy/lingbot_vla_policy.py:119` | **部署封装** |
| `LingbotVLAServer.infer` | 同上 | **推理唯一入口** |
| `FeatureTransform` | `lingbotvla/data/vla_data/utils.py:37` | 特征双向映射 + 归一化 |
| `VLADataset` | `lingbotvla/data/vla_data/base_dataset.py` | LeRobot v3.0 数据集读取 |
| `build_foundation_model` 等 | `lingbotvla/models/` | 模型与处理器构建工厂 |
| `init_parallel_state` | `lingbotvla/distributed/` | FSDP2/TP/EP/CP/ulysses 并行初始化 |

## 输入/输出契约

### 模型层 `sample_actions`

- `images`: `[B, num_cams, 3, H, W]`
- `img_masks`: `[B, num_cams]`
- `lang_tokens` / `lang_masks`: `[B, L]`，`tokenizer_max_length=72`
- `state`: `[B, max_state_dim]`，默认 `max_state_dim=75`
- 返回 `actions`: `[B, n_action_steps, max_action_dim]`，`n_action_steps=50`

### 部署层 `LingbotVLAServer.infer(observation)`

输入 observation（WebSocket msgpack，numpy）：图像、状态、任务指令、`robo_name`、`reset`。

输出 action_chunk：`{action_feature: [use_length, dim] float32 numpy}`。

## 依赖关系

### 对 lingbot 其他子项目

- **lingbot-depth**：以 **git 子模块**形式引入，仅深度版模型用于深度蒸馏/对齐

### 外部依赖

- **基座权重**：Qwen2.5-VL-3B-Instruct（必需）、MoGe-2-vitb-normal 与 LingBot-Depth（仅深度版）
- **核心库**：Python 3.12、PyTorch 2.8.0、CUDA 12.8、transformers 4.51.3、flash-attn 2.8.3、lerobot v0.4.2

### 模型分发

| 模型 | 说明 |
|------|------|
| `lingbot-vla-4b` | 预训练（无深度） |
| `lingbot-vla-4b-depth` | 预训练（深度蒸馏） |
| `lingbot-vla-4b-posttrain-robotwin` / `-depth-posttrain-robotwin` | RoboTwin 后训练权重 |

## 常用命令

```bash
# 安装
bash install.sh

# 下载预训练权重
python3 scripts/download_hf_model.py --repo_id robbyant/lingbot-vla-4b --local_dir lingbot-vla-4b

# 后训练
bash train.sh tasks/vla/train_lingbotvla.py ./configs/vla/robotwin_load20000h.yaml \
    --data.train_path /path/to/data --data.data_name robotwin \
    --data.norm_stats_file assets/norm_stats/robotwin_50.json --train.output_dir output/

# 部署
export QWEN25_PATH=path_to_Qwen2.5-VL-3B-Instruct
python -m deploy.lingbot_vla_policy --model_path <ckpt>/hf_ckpt \
    --use_compile --use_length 25 --port 8006 --num_denoising_step 10
```

## 特殊约定

- 环境变量 `QWEN25_PATH`：推理/评估必须设置
- 推理 ckpt 目录必须同时包含 `*.safetensors`、`config.json`、`lingbotvla_cli.yaml`
- 训练用 flash-attention-2；推理强制 `attention_implementation='eager'`
- 部署默认 bf16，可选 fp32
- 旧权重兼容：2026/05/01 前权重因 LeRobot v2.1→v3.0 迁移可能报错

## 相关链接

- 父项目：[[06_Projects/external/lingbot/index|LingBot]]
- 深度模型：[[06_Projects/external/lingbot/lingbot-depth|LingBot-Depth]]
- 第二代 VLA：[[06_Projects/external/lingbot/lingbot-vla-v2|LingBot-VLA-V2]]
- 环境分析：[[06_Projects/external/lingbot/python-env-analysis|LingBot Python 环境差异分析]]
