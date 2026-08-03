---
title: "LingBot Python 环境差异分析"
description: "lingbot 五子项目 Python/PyTorch/依赖版本冲突与分组建议"
tags: [project, lingbot, python, environment, dependency]
created: 2026-07-28
source: "/home/kemove/INNOV/projects/lingbot"
---

# LingBot Python 环境差异分析

分析日期：2026-07-28。输入：各子项目 `pyproject.toml` / `requirements.txt` / `setup.py` / `Makefile` / `INSTALL.md` / `README` / `install.sh` / `tools/create_train_env.sh`。

## 环境要求总览

| 项目 | Python | PyTorch | CUDA | transformers | flash-attn | xformers | lerobot | 其他关键约束 |
|---|---|---|---|---|---|---|---|---|
| lingbot-depth | >=3.9 | **torch==2.6.0** 钉死 | 未指定 | 无依赖 | 无 | **xformers==0.0.29.post2** 钉死 | 无 | opencv-python、trimesh |
| lingbot-va | ==3.10.16 | **torch==2.9.0**（cu126） | **CUDA 12.6** | ==4.55.2 | 不钉版本 | 无 | **lerobot==0.3.3** | diffusers==0.36.0、numpy==1.26.4 |
| lingbot-vla | 3.12 | **torch==2.8.0** | **CUDA 12.8** | **==4.51.3** | **flash-attn==2.8.3** | 无 | **lerobot v0.4.2** | torchvision==0.23.0、torchcodec==0.6.0 |
| lingbot-vla-v2 | 3.12 | **torch==2.8.0** | 随 torch 2.8 | **==4.57.3** | **flash-attn==2.8.3** | 无 | **lerobot v0.4.2** | torchvision==0.23.0、qwen-vl-utils==0.0.11 |
| lingbot-world-v2 | >=3.10 | torch>=2.4.0 | 未指定 | **>=4.49.0 且 <=4.51.3** | 不钉版本 | 无 | 无 | diffusers>=0.31.0、numpy<2 |

## 核心冲突点

1. **PyTorch 版本三足鼎立**：depth（2.6.0）、vla/vla-v2（2.8.0）、va（2.9.0）
2. **xformers 钉死**：depth 独有，与 torch 2.6.x 绑定
3. **flash-attn ABI 绑定**：跟随 torch 版本
4. **transformers 区间互斥**：vla-v2（4.57.3）与 world-v2（<=4.51.3）无解
5. **lerobot 版本分裂**：va（0.3.3）与 vla/vla-v2（0.4.2）数据格式不兼容

## 结论

**不能共用一个环境。** 推荐分 4 个环境：

| 环境 | 项目 | 配置 |
|---|---|---|
| env-A：vla 系 | lingbot-vla + lingbot-vla-v2 | Python 3.12 + torch 2.8.0 (cu128) + flash-attn 2.8.3 + lerobot 0.4.2 |
| env-B：va | lingbot-va | Python 3.10 + torch 2.9.0 (cu126) + transformers 4.55.2 + lerobot 0.3.3 |
| env-C：depth | lingbot-depth | Python 3.9+ + torch 2.6.0 + xformers 0.0.29.post2 |
| env-D：world-v2 | lingbot-world-v2 | Python 3.10+ + torch>=2.4 + transformers<=4.51.3 |

## 相关链接

- 父项目：[[06_Projects/external/lingbot/index|LingBot]]
- 子项目：[[06_Projects/external/lingbot/lingbot-depth|LingBot-Depth]]、[[06_Projects/external/lingbot/lingbot-va|LingBot-VA]]、[[06_Projects/external/lingbot/lingbot-vla|LingBot-VLA]]、[[06_Projects/external/lingbot/lingbot-vla-v2|LingBot-VLA-V2]]、[[06_Projects/external/lingbot/lingbot-world-v2|LingBot-World-V2]]
