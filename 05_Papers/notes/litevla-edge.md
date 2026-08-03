---
title: "LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics"
description: "面向嵌入式机器人的量化端侧多模态 VLA 控制方案。"
tags: ["VLA", "Edge-Deployment", "Quantization", "Jetson-Orin", "ROS2", "llama.cpp", "GGUF"]
created: 2026-07-15
---

# LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics

## 基本信息
- **作者**: Justin Williams, Kishor Datta Gupta, Roy George (Clark Atlanta University), Mrinmoy Sarkar (Siemens Corporation)
- **机构**: Clark Atlanta University, Siemens Corporation
- **链接**: [arXiv:2603.03380](https://arxiv.org/abs/2603.03380)
- **发表**: arXiv preprint, 2026

## 研究背景与动机

VLA 模型（如 PaLM-E, RT-2, OpenVLA）实现了视觉感知、语言理解和动作生成的统一，但参数规模巨大（>7B），需要云端或高端 GPU 推理，无法在功率受限的嵌入式机器人场景中部署。

LiteVLA 此前在 Raspberry Pi 上验证了极端边缘部署的可行性，但存在**多秒级推理延迟**，只能进行异步开环执行。本文的 **LiteVLA-Edge** 旨在将 VLA 从"审慎推理"推进到**实时 visuomotor 控制**，核心目标是降低延迟、实现闭环控制。

## 核心方法

### 系统架构

采用模块化 perception-reasoning-action 管线：

1. **Vision Encoder**：处理 RGB 图像帧，提取视觉 token
2. **Multimodal Transformer**：基于 SmolVLM-256M 蒸馏版本，融合视觉 token 与语言目标上下文
3. **Action Decode**：将多模态表示解码为结构化动作指令
4. **ROS 2 Bridge**：通过 `geometry_msgs/Twist` 接口发布速度指令，100 Hz 底层控制器保持稳定

### 训练与压缩

- **监督微调**：在机器人演示数据集上进行 image-to-action 监督学习，使用 LoRA (r=8, α=8) 在 FP32 精度下训练
- **后训练量化**：FP32 权重 → GGUF 格式 → 4-bit 量化 (Q4_K_M)，大幅减小模型体积
- **目标函数**：
  $$\mathcal{L}_{SFT} = -\sum_{i=1}^{n} \log P(a_i | a_{<i}, I_t, g; \theta)$$

### 边缘推理部署

- **硬件**：NVIDIA Jetson AGX Orin (64GB)
- **运行时**：llama.cpp + CUDA backend
- **配置**：全部 42 层 transformer 卸载到 GPU，n_ctx=512，最大输出 12 tokens
- **结果**：平均推理延迟 **150.5 ms（约 6.6 Hz）**，标准差仅 0.125 ms

![[99_Attachments/papers/images/litevla-edge/litevla_edge_fig1_architecture.jpg]]

## 关键创新点

- **系统工程贡献**：首次在 Jetson AGX Orin 上实现 VLA 的 100% 本地推理，达到 6.6 Hz 闭环控制
- **量化稳定性**：证明 4-bit GGUF 量化不会导致"动作漂移"，actions 保持稳定
- **低抖动**：推理延迟标准差 0.125 ms，保证了 ROS 2 控制心跳的确定性
- **模块化设计**：感知-推理-动作模块解耦，支持确定性 safety override

## 实验结果

### 硬件基准对比

| Model | Type | Params | Hardware | Closed-Loop |
|-------|------|--------|----------|-------------|
| Moondream2 | VLM | ~2B | CPU/Edge GPU | No |
| OpenVLA | VLA | 7B | RTX 4090 | Partial (~5 Hz) |
| EdgeVLA | VLA | ~1B | A100-40GB | Yes (~10 Hz) |
| **LiteVLA-Edge** | **VLA** | **256M** | **Jetson AGX Orin** | **Yes (6.6 Hz)** |

### 端到端推理性能（Jetson Orin NX, 300 runs）

| 指标 | 结果 |
|------|------|
| 平均延迟 | 150.5 ms |
| 标准差 | 0.13 ms |
| 最小/最大 | 150.4 / 151.0 ms |
| 推理频率 | 6.64 Hz |

### 定性转变

从 >1s 的"开环"（停-想-动）转变为 150ms 级别的"闭环"（边动边调整），足以支持 visual servoing 和动态环境中的实时轨迹修正。

## 个人思考与启发

1. **"够用就好"的设计哲学**：不追求新策略目标或控制律，而是专注解决实际部署问题。256M 参数 + 4-bit 量化 + 边缘 GPU 的组合提供了一个实用参考点。

2. **与 LiteVLA-H 的关系**：本文是 LiteVLA 系列的基础工作，建立了边缘部署基线（6.6 Hz）。后续 LiteVLA-H 进一步将动作分支提升到 19.74 Hz 并引入双速率调度。

3. **量化在机器人中的特殊性**：不同于 LLM 的量化主要关注文本质量，机器人 VLA 的量化需要额外验证动作精度和时序稳定性。

4. **可改进方向**：
   - 当前仅验证延迟和抖动，缺乏标准化任务基准上的成功率评估
   - 论文自身也承认了 validity threat：缺乏任务级对比评估
   - 可探索与 FASTER、VLA-Perf 等框架的集成，进行更系统的延迟归因
   - 混合精度策略（关键层 FP16 + 其余 INT4）可能进一步提升速度

5. **与 LLM 边缘部署的对比**：VLA 边缘部署比 LLM 更具挑战，不仅需要低延迟，还需要确定性时序和动作稳定性

## 相关论文

- LiteVLA: Efficient Vision-Language-Action Control on CPU-bound Edge Robots (arXiv:2511.05642)
- LiteVLA-H: Dual-Rate VLA Inference for Onboard Aerial Guidance (arXiv:2605.00884)
- EdgeVLA: Efficient Vision-Language-Action Models (arXiv:2507.14049)
- SmolVLA: A VLA Model for Affordable and Efficient Robotics (arXiv:2506.01844)
- OpenVLA: An Open-Source Vision-Language-Action Model (arXiv:2406.09246)


## 原文

[[05_Papers/articles/litevla-edge|litevla-edge]]
