---
title: "H2R: Human-to-Robot Data Augmentation for Robot Pre-training from Videos"
description: "将第一人称人手视频通过 3D 重建与图像修复替换为机器人手臂，缩小视觉预训练中人与机器人之间的域差距。"
tags: ["具身智能", "Robot Learning", "Data Augmentation", "Imitation Learning", "Vision Pre-training"]
created: 2026-07-28
---

# H2R: Human-to-Robot Data Augmentation for Robot Pre-training from Videos

## 基本信息
- **作者**: Guangrun Li, Yaoxu Lyu, Zhuoyang Liu, Chengkai Hou, Jieyu Zhang, Shanghang Zhang
- **机构**: 北京大学多媒体信息处理国家重点实验室、华盛顿大学
- **链接**: https://arxiv.org/abs/2507.11978
- **发表**: arXiv, 2025

![[99_Attachments/papers/images/h2r/d5a4428a0c2a1af0042a29a5db5eaf73621b2e0dd03044a2e323bd4f9ab38048.jpg]]

## 研究背景与动机

大规模第一人称人手视频（Ego4D、SSv2 等）被广泛用于机器人视觉预训练，但存在两个核心问题：

1. **视觉域差距**: 人手与机器人末端执行器在外观、运动学上差异显著，预训练编码器直接迁移到机器人任务时性能受限。
2. **机器人数据采集成本高**: 真实机器人演示数据昂贵且规模有限，难以支撑大规模预训练。

已有方法（WHIRL、RoVi-Aug、EgoMimic）多从视角对齐或外观增强入手，未显式将人手动作语义保留并替换为真实机器人形态。

## 核心贡献

### 1. H2R 数据增强管线
- 将第一人称人手视频转换为机器人中心视角的视觉序列。
- 保留原视频中人与物体的交互语义，但视觉外观替换为目标机器人手臂。

### 2. 三阶段处理流程
- **手部姿态估计**: 使用 HaMeR 重建 3D 人手关键点与相机内外参。
- **重定向**: 将人手关键点映射到机器人关节角，并在仿真器中对齐相机视角。
- **移除与修复**: 用 SAM 分割人手，LaMa 修复背景，再将渲染的机器人手臂像素级叠加到原位置。

### 3. 可扩展的质量评估指标
- 提出基于 CLIP 的图像-文本相似度指标，量化增强后机器人帧与原动作语义的一致性。

## 方法

### 整体流程

```
人手视频
    ↓ HaMeR (3D hand pose + camera params)
人手关键点 + 相机参数
    ↓ Retargeting
机器人关节角 + 仿真器相机位姿
    ↓ SAM 分割 + LaMa 修复
去除人手的背景图
    ↓ Pixel-level alignment & overlay
机器人中心增强视频
```

### 关键步骤

| 步骤 | 输入 | 输出 | 工具 |
|------|------|------|------|
| Hand Pose Estimation | RGB 帧 | 人手关键点、相机内外参 | HaMeR |
| Retargeting | 人手关键点、相机参数 | 机器人关节角、仿真器相机位姿 | 自定义运动学映射 |
| Removal & Inpainting | 原图 + 人手掩码 | 无手的背景图 | SAM + LaMa |
| Overlay | 修复背景 + 渲染机器人 | 增强帧 | 像素级对齐合成 |

### 相机对齐
- 建立人手坐标系 $C_H$ 与机器人坐标系 $C_S$。
- 通过旋转矩阵将真实相机位姿变换到仿真器相机位姿，保证叠加机器人手臂与原人手在像素空间对齐。

## 实验与结论

### 预训练设置
- **编码器**: MAE、R3M（ViT-Base）
- **预训练数据**: SSv2（约 1M 帧）、Ego4D（117K clips，约 1M 帧）
- **增强机器人形态**: UR5 + Robotiq Gripper、UR5 + Leaphand、Franka + Robotiq Gripper

### 仿真结果
- 在 Robomimic、RLBench、PushT、CortexBench 四个基准上测试。
- H2R 在 MAE 上平均提升 **1.3%–10.2%**，R3M 上也有稳定增益。
- 与真实机器人数据集 DROID 预训练相比，H2R 在 Robomimic 上表现更优（R3M-H2R 61.3% vs R3M-DROID 56.7%）。

### 真实世界结果
- 在 UR5-Gripper、UR5-Leaphand、双 Franka、双 UR5e 上验证。
- H2R 在真实任务中成功率提升 **3.3%–23.3%**。
- 灵巧手（Leaphand）任务收益最显著，ACT 策略下 R3M 提升达 23.3%。

### 跨形态泛化
- 用 UR5 形态增强预训练，下游使用不同机器人（Leaphand）仍能获得显著提升。
- 说明 H2R 的收益不完全依赖预训练与下游机器人形态一致。

### VLA 兼容性
- 将 H2R 增强数据用于微调 UVA 的 VAE 视觉主干，在双 UR5e 任务上成功率从 0.20 提升到 0.35。

### 消融实验
- **w/o Overlay**: 仅去除人手不叠加机器人，性能大幅下降（丢失关键交互像素）。
- **w/o Retargeting**: 随机粘贴机器人臂而非精确重定向，性能明显下降。
- 证明精确重定向与机器人外观替换都是必要的。

## 个人思考

- **工程价值高**: H2R 是一个轻量级、模块化的数据增强方案，可叠加到现有人体视频预训练流程中，无需重新采集机器人数据。
- **关键假设**: 依赖 HaMeR 的手部重建精度、SAM 的分割质量以及 LaMa 的修复效果；对于遮挡严重或快速运动场景可能失效。
- **泛化潜力**: 跨形态实验说明学到的表示对机器人形态具有一定不变性，但不同末端执行器（夹爪 vs 灵巧手）间的迁移仍有边界。
- **与 VLA 的结合**: 作为视觉预训练/微调的数据来源，H2R 可直接服务于 VLA 模型的视觉 backbone 训练。

## 相关论文
- [[04_Embodied-AI/VLA/Diffusion-Policy|Diffusion Policy]]
- [[ACT]]
- [[R3M]]
- [[MAE]]
- [[UVA]]
- [[EgoMimic]]
- [[RoVi-Aug]]
- [[DROID]]

## 原文

[[05_Papers/articles/h2r|h2r]]
