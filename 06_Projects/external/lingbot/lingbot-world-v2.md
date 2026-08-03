---
title: "LingBot-World-V2"
description: "可交互视频世界模型（Wan2.2 因果扩散），单图+文本+相机轨迹生成无界交互视频"
tags: [project, lingbot, embodied-ai, world-model, video-generation]
created: 2026-07-28
source: "/home/kemove/INNOV/projects/lingbot/lingbot-world-v2"
---

# LingBot-World-V2

LingBot-World 2.0（LingBot-World-Infinity）是一个**可交互视频世界模型**（基于 Wan2.2 构建的因果扩散模型），从单张图像 + 文本提示 + 相机轨迹出发，逐块（chunk-by-chunk，带 KV Cache）自回归生成无界长度的交互式视频。

## 项目定位

- 仓库路径：`/home/kemove/INNOV/projects/lingbot/lingbot-world-v2/`
- 特性：无界交互时长（因果预训练）、实时变体蒸馏（720p@60fps 目标）、多样化动作/文本事件
- 论文：arXiv:2607.07534《Infinite Worlds with Versatile Interactions》
- 权重渠道：`robbyant/lingbot-world-v2-14b-causal-fast`
- 本仓库仅含推理代码，无训练代码、无部署代码
- 许可：CC BY-NC-SA 4.0（仅非商用）

## 目录结构

```text
lingbot-world-v2/
├── generate.py                  # 唯一推理入口
├── run_fast.sh                  # causal_fast 8 卡示例脚本
├── wan/                         # 核心包
│   ├── image2video.py           # WanI2VCausal 推理流水线
│   ├── configs/                 # 配置注册表与公共配置
│   ├── modules/                 # DiT、注意力、T5、VAE
│   ├── distributed/             # FSDP、序列并行、Ulysses
│   └── utils/                   # 相机工具、Flow Matching 调度器、通用工具
├── examples/                    # 6 个示例
└── pyproject.toml / requirements.txt / Makefile
```

## 核心类/函数/入口

| 符号 | 位置 | 职责 |
|---|---|---|
| `generate(args)` | `generate.py` | CLI 主入口 |
| `WanI2VCausal` | `wan/image2video.py` | 推理流水线主类 |
| `WanI2VCausal.generate()` | 同上 | 统一入口，按 `infer_mode` 分发 |
| `_generate_causal_fast` | 同上 | 蒸馏少步采样，chunk 间滑窗 KV Cache |
| `_generate_causal_pretrain` | 同上 | 预训练因果模型 40 步 CFG 采样 |
| `WanI2VCausal.prewarm()` | 同上 | 可选预热，消除首个 chunk CUDA/NCCL 冷启动 |
| `WanModelFast` | `wan/modules/model_fast.py` | 蒸馏 DiT：局部注意力 + sink KV Cache |
| `WanModelCausal` | `wan/modules/model_causal.py` | 因果预训练 DiT：完整 KV Cache |
| `FlowUniPCMultistepScheduler` | `wan/utils/fm_solvers_unipc.py` | Flow Matching UniPC 采样调度 |
| `get_plucker_embeddings` | `wan/utils/cam_utils.py` | 生成逐像素 Plücker 射线嵌入 |
| `WAN_CONFIGS` | `wan/configs/__init__.py` | 配置注册表 |

## 输入/输出契约

### 顶层 API：`WanI2VCausal.generate(input_prompt, img, action_path, ...)`

- `input_prompt: str` — 文本提示，经 umt5-xxl 编码，最长 512 token
- `img: PIL.Image` — 起始帧图像，RGB
- `action_path: str` — **必填**，目录须包含 `poses.npy` 与 `intrinsics.npy`
- 关键参数：
  - `frame_num: int` — 必须为 `4n+1`（默认 81）
  - `chunk_size: int` — 每次 DiT 前向的 latent 帧块大小（默认 4）
  - `max_area: int` — 像素面积（如 480*832）
  - `local_attn_size` / `sink_size` — KV Cache 滑窗 / sink 大小
- 输出：`torch.Tensor (C=3, F, H, W)`，值域 [-1,1]

### 内部张量形状（causal_fast 路径）

- VAE：`vae_stride = (4, 8, 8)`，latent 通道 16
- 条件 `y` → 20 通道；DiT 输入 36 通道
- DiT（A14B）：dim=5120，heads=40，layers=40，patch=(1,2,2)

## 依赖关系

- 与 lingbot 其他子项目：**无代码级依赖**，独立仓库
- 基座：Wan2.2
- 外部库：torch >= 2.4.0、torchvision、diffusers >= 0.31.0、transformers 4.49~4.51.3、flash_attn、imageio[ffmpeg]、scipy、numpy < 2
- Python >= 3.10

## 常用命令

```bash
# 安装
pip install -r requirements.txt
pip install flash-attn --no-build-isolation

# 8 卡推理
bash run_fast.sh lingbot-world-v2-14b-causal-fast 361

# 单卡
python generate.py --task i2v-A14B --size 480*832 --ckpt_dir <weights> \
  --image examples/04/image.jpg --action_path examples/04 --frame_num 81

# 格式化
make format
```

## 特殊约定

- `--task` 仅支持 `i2v-A14B`
- 支持分辨率：`720*1280 / 1280*720 / 480*832 / 832*480`（`--size` 为 `高*宽`）
- `ulysses_size` 必须等于 `world_size` 且整除 `num_heads=40`
- 动作输入当前以相机轨迹为主，键盘动作通道为预留接口
- T5 缓存按 prompt sha256 键控，可用 `clear_text_cache()` 清理
- 输出视频 fps 固定 16

## 相关链接

- 父项目：[[06_Projects/external/lingbot/index|LingBot]]
- 环境分析：[[06_Projects/external/lingbot/python-env-analysis|LingBot Python 环境差异分析]]
