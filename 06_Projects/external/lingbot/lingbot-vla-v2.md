---
title: "LingBot-VLA-V2"
description: "第二代 VLA 模型，基于 Qwen3-VL-4B + MoE 动作专家，55 维统一动作空间"
tags: [project, lingbot, embodied-ai, vla, robot-learning]
created: 2026-07-28
source: "/home/kemove/INNOV/projects/lingbot/lingbot-vla-v2"
---

# LingBot-VLA-V2

蚂蚁灵波科技第二代视觉-语言-动作（VLA）基础模型：基于 Qwen3-VL-4B 主干 + MoE 动作专家，通过流匹配（Flow Matching）输出动作块，支持 20 种机器人构型的统一 55 维动作空间，并以 LingBot-Depth / DINO-Video 双查询蒸馏注入几何与时序先验。Python 包名为 `lingbotvla`（Apache-2.0）。

## 项目定位

- 仓库路径：`/home/kemove/INNOV/projects/lingbot/lingbot-vla-v2/`
- 相比 V1 升级：
  - 数据管线：约 6 万小时预训练数据
  - 动作空间：统一表征覆盖手臂/末端执行器/夹爪/灵巧手/腰/头/移动底盘
  - 预测动力学：未来帧预测作为代理任务（depth + video 蒸馏）
- 预训练权重：`robbyant/lingbot-vla-v2-6b`

## 目录结构

```text
lingbot-vla-v2/
├── lingbotvla/                 # 核心 Python 包
│   ├── models/vla/
│   │   ├── lingbot_vla/        # V1/V2 主模型
│   │   └── vision_models/      # 蒸馏教师与视觉模型
│   ├── data/                   # VLA 数据集与多模态预处理
│   ├── distributed/            # FSDP1/FSDP2、Ulysses、MoE EP
│   ├── checkpoint/             # 分布式 checkpoint
│   ├── optim/  schedulers/     # 优化器与 LR 调度
│   └── utils/                  # 参数、日志、异步保存
├── tasks/vla/train_lingbotvla.py  # 训练主入口
├── deploy/                     # 推理/WebSocket 部署
├── scripts/                    # 下载、统计、开环评估
├── configs/                    # 训练配置 + 机器人配置
├── experiment/robotwin/        # 仿真评测脚本
├── tools/create_train_env.sh   # conda 环境搭建
└── train.sh                    # torchrun 包装
```

## 核心类/函数/入口

| 符号 | 位置 | 职责 |
|------|------|------|
| `LingbotVlaV2Policy` | `models/vla/lingbot_vla/modeling_lingbot_vla_v2.py:1198` | V2 顶层策略模型（HF PreTrainedModel） |
| `FlowMatchingV2` | 同上 :767 | 流匹配核心：训练 loss 与推理采样 |
| `QwenvlWithExpertV2Model` | 同上 :121 | Qwen3-VL 前缀 + 动作专家的融合主干 |
| `LingbotVLAV2Config` | `configuration_lingbot_vla.py:181` | V2 配置 |
| `main()` | `tasks/vla/train_lingbotvla.py:332` | 训练唯一入口 |
| `LingBotVlaV2InferencePolicy` / `LingbotVLAv2Server` | `deploy/lingbot_vla_v2_policy.py` | 推理封装 + websocket 服务 |
| `build_depth_model` / `build_video_model` | `models/vla/vision_models/module_utils.py` | 构建蒸馏教师并生成蒸馏目标 |
| `FeatureTransform` | `data/vla_data/utils.py` | 状态/动作归一化与反归一化 |
| `build_foundation_model` / `build_processor` | `lingbotvla/models/` | 按 config_key 构建模型与处理器 |
| `build_parallelize_model` / `init_parallel_state` | `lingbotvla/distributed/` | FSDP/并行初始化 |
| `build_moe_load_balance_hook` | `moe_load_balance.py` | loss-free 负载均衡 hook |

## 输入/输出契约

### 模型推理：`FlowMatchingV2.sample_actions`

- `images`: `(B, n_cam, C, H, W)` 多视角图像
- `img_masks`: 相机有效掩码
- `lang_tokens` / `lang_masks`: 指令 token 序列（默认长度 48）
- `state`: `(B, max_state_dim)` 归一化后的机器人状态
- 输出：`actions`: `(B, n_action_steps, max_action_dim)`，`n_action_steps=50`，去噪步数 `num_steps=10`

### 统一动作空间（canonical，最多 55 维）

| 分量 | 维度 |
|------|------|
| arm.position（关节角） | 14 |
| end.position（末端位姿） | 14 |
| effector.position（夹爪） | 2 |
| hand.position（灵巧手） | 12 |
| waist.position | 4 |
| head.position | 2 |
| base.position（移动底盘） | 3 |
| 预留 | 4 |

## 依赖关系

### 对 lingbot 其他子项目

- **lingbot-depth**：以 vendored 形式内嵌于 `models/vla/vision_models/lingbot-depth/`（MoRGBD 深度教师），权重从 HF 下载。代码自包含，不依赖外部 lingbot-depth 仓库。

### 关键外部依赖

- 基础模型：**Qwen3-VL-4B-Instruct**
- 教师模型：MoGe-2-vitb-normal、LingBot-Depth、DINO-VIDEO checkpoint
- 框架：PyTorch 2.8.0、transformers 4.57.3、flash-attn 2.8.3、LeRobot、qwen-vl-utils
- Python 3.12

## 常用命令

```bash
# 环境搭建
bash tools/create_train_env.sh [--env-name lingbotvla] [--recreate]

# 下载预训练权重
python3 scripts/download_hf_model.py --repo_id robbyant/lingbot-vla-v2-6b --local_dir lingbot-vla

# 后训练
bash train.sh tasks/vla/train_lingbotvla.py ./configs/vla/robotwin/robotwin.yaml \
  --data.train_path assets/training_data/robotwin.txt \
  --data.data_name multi --train.output_dir output/

# 真机部署
export QWEN3VL_PATH=path_to_Qwen3-VL-4B-Instruct
python -m deploy.lingbot_vla_v2_policy --model_path <ckpt> \
  --use_compile --use_length 25 --port <port>

# 质量检查 / 测试
make quality
make test
```

## 特殊约定

- 环境变量 `QWEN3VL_PATH`（部署/评测）与 `QWEN3_PATH`（open_loop_eval）
- MoE：36 层全 MoE，32 专家 top-4，`moe_implementation: fused`
- 优化器：默认 AdamW，可切 Muon
- 蒸馏：`train.align_params` 控制 depth / future-depth / future-video 蒸馏
- 并行：`data_parallel_mode: fsdp2`，支持 ulysses 序列并行与 EP
- 论文：arXiv:2607.06403

## 相关链接

- 父项目：[[06_Projects/external/lingbot/index|LingBot]]
- 深度模型：[[06_Projects/external/lingbot/lingbot-depth|LingBot-Depth]]
- 第一代 VLA：[[06_Projects/external/lingbot/lingbot-vla|LingBot-VLA]]
- 环境分析：[[06_Projects/external/lingbot/python-env-analysis|LingBot Python 环境差异分析]]
