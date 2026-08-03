---
title: "LingBot-Depth"
description: "基于 Masked Depth Modeling 的空间感知基础模型，将噪声/残缺深度精炼为度量精确的 3D 深度"
tags: [project, lingbot, embodied-ai, depth-estimation, robot-learning]
created: 2026-07-28
source: "/home/kemove/INNOV/projects/lingbot/lingbot-depth"
---

# LingBot-Depth

基于 Masked Depth Modeling（掩码深度建模）的空间感知基础模型：将不完整、带噪声的深度传感器数据精炼为高质量、度量精确的 3D 深度测量，服务于机器人学习与 3D 视觉下游任务（深度补全、场景重建、4D 点跟踪、灵巧抓取）。论文已接收于 ECCV 2026。

## 项目定位

- 仓库路径：`/home/kemove/INNOV/projects/lingbot/lingbot-depth/`
- 核心任务：深度精炼、深度补全、场景重建
- 模型分发：Hugging Face / ModelScope `robbyant/lingbot-depth-*`
- 许可：Apache-2.0
- 相关项目：被 [[06_Projects/external/lingbot/lingbot-vla|lingbot-vla]] 以 git 子模块引入，被 [[06_Projects/external/lingbot/lingbot-vla-v2|lingbot-vla-v2]] 以 vendored 形式内嵌

## 目录结构

```text
lingbot-depth/
├── example.py                  # 推理示例入口（CLI），唯一推荐调用入口
├── examples/                   # 8 组示例数据（0-7），含 rgb.png / raw_depth.png / intrinsics.txt
├── mdm/                        # 核心 Python 包（pip 包名 mdm）
│   ├── model/
│   │   ├── v2.py               # MDMModel 主模型定义（当前唯一模型版本）
│   │   ├── modules_rgbd_encoder.py  # DINOv2_RGBD_Encoder：RGB-D 融合编码器
│   │   ├── modules_decoder.py       # ConvStack：neck 与 depth/mask 解码头
│   │   ├── utils.py                 # 模型工具（SDPA 包装、梯度检查点、depth_to_pointcloud）
│   │   └── dinov2_rgbd/             # 改造自 DINOv2 的 backbone
│   └── utils/
│       ├── geo.py              # 几何工具
│       ├── io.py               # 读写
│       ├── tools.py            # 通用工具
│       └── vis.py              # 深度/点云可视化
├── pyproject.toml
├── requirements.txt
├── tech-report.pdf
└── README.md / LICENSE / LEGAL.md
```

## 核心类/函数/入口

| 符号 | 位置 | 职责 |
|------|------|------|
| `MDMModel` | `mdm/model/v2.py` | 主模型类（encoder + neck + depth_head/mask_head） |
| `MDMModel.from_pretrained` | `mdm/model/v2.py:68` | 加载模型：本地路径或 HF repo（自动下载 model.pt） |
| `MDMModel.infer` | `mdm/model/v2.py:171` | **推理唯一入口**：输入 RGB/深度/内参，输出 depth/points/mask |
| `MDMModel.forward` | `mdm/model/v2.py:98` | 前向：编码→neck→head→重映射输出 |
| `DINOv2_RGBD_Encoder` | `mdm/model/modules_rgbd_encoder.py` | RGB-D 双模态 ViT 编码器 |
| `ConvStack` | `mdm/model/modules_decoder.py` | 解码器/neck 卷积堆叠 |
| `depth_to_pointcloud` | `mdm/model/utils.py:68` | 深度图反投影为点云 |
| `normalized_view_plane_uv` | `mdm/utils/geo.py` | 生成归一化 UV 平面坐标 |

### 输入/输出契约（`model.infer`）

- `image`: RGB tensor `[B,3,H,W]`，float32，[0,1]
- `depth_in`: 深度 tensor `[B,H,W]`，单位米，无效区域为 0 或 NaN
- `intrinsics`: `[B,3,3]`，**归一化内参**（fx/W, fy/H, cx/W, cy/H）
- 参数：`num_tokens`、`resolution_level=9`、`apply_mask=True`、`use_fp16=True`
- 返回 dict：`{'depth': [B,H,W], 'points': [B,H,W,3] 相机系点云, 'mask': 二值掩码}`（仅含非 None 项）

## 依赖关系

- **对其他 lingbot 子项目**：无代码级依赖，独立仓库。数据集含 RobbyVla（VLA 机器人操作数据），但仅为数据来源，不引入代码。
- **外部库**（pyproject.toml）：torch==2.6.0、torchvision、xformers==v0.0.29.post2、opencv-python、scipy、matplotlib、trimesh、pillow、huggingface_hub、numpy、click。Python ≥ 3.9。
- **上游基座**：DINOv2（facebookresearch），backbone 代码改造自 DINOv2；思想继承 MAE。

### 可用预训练模型

| 模型 | HF repo | 说明 |
|------|---------|------|
| LingBot-Depth-v0.5 | `robbyant/lingbot-depth-pretrain-vitl-14-v0.5` | 推荐，通用深度精炼与补全 |
| LingBot-Depth-v0.1 | `robbyant/lingbot-depth-pretrain-vitl-14` | 通用深度精炼 |
| LingBot-Depth-DC | `robbyant/lingbot-depth-postrain-dc-vitl14` | 稀疏深度补全优化 |

## 常用命令

```bash
# 安装
conda create -n lingbot-depth python=3.9 && conda activate lingbot-depth
python -m pip install -e .

# 推理（首次运行自动从 HF 下载模型）
python example.py                                  # 默认处理 examples/0
python example.py --example 1                      # 指定示例 0-7
python example.py --model robbyant/lingbot-depth-postrain-dc-vitl14  # 换模型
python example.py --output my_results              # 自定义输出目录（默认 result/）
```

输出到 `result/`：`rgb.png`、`depth_input/refined.npy`、`depth_input/refined.png`、`depth_comparison.png`、`point_cloud.ply`。

## 特殊约定

- **归一化内参约定**：内参矩阵必须按图像宽高归一化（fx/W、fy/H、cx/W、cy/H）。
- **深度单位**：米；原始 PNG 深度按毫米存储时需 `/1000.0` 转换。
- **无效深度**：用 0 或 NaN 表示。
- **掩码语义**：`apply_mask=True` 时无效区域输出 `torch.inf`。
- **推理精度**：默认 bf16 autocast（use_fp16 参数名但实际用 bfloat16），输出转回 fp32。
- **代码风格**：禁止函数内联导入，导入一律在文件顶部；注释用中文、1-2 行只写核心功能与 API 契约。

## 相关链接

- 父项目：[[06_Projects/external/lingbot/index|LingBot]]
- 环境分析：[[06_Projects/external/lingbot/python-env-analysis|LingBot Python 环境差异分析]]
- 消费方：[[06_Projects/external/lingbot/lingbot-vla|lingbot-vla]]、[[06_Projects/external/lingbot/lingbot-vla-v2|lingbot-vla-v2]]
