---
title: "Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data"
description: "从第一视角人体操作视频合成大规模机器人训练数据：动作重定向、视觉对齐、多形态渲染与解耦泛化评估。"
tags: [embodied-ai, robot-learning, data-synthesis, egocentric-video, cross-embodiment]
created: 2026-08-06
---

# Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data

## 基本信息

- **作者**: Ye Wang, Pei Lin, Xiong-Hui Chen, Haoqi Yuan, Zhixuan Liang, Yiyang Huang, Anzhe Chen, Zixing Lei, Jie Zhang, Tao Zhang, Haoyang Li, Tong Zhang, Chenxi Xiao, Ziyuan Jiao, Qin Jin
- **机构**: AIM3 Lab (Renmin University), Qwen Team (Alibaba), ShanghaiTech, BIGAI, BUAA
- **链接**: [arXiv:2608.02580v1](https://arxiv.org/abs/2608.02580v1)
- **发表**: 2026-08-03
- **原文**: [[05_Papers/articles/ego2robot.md|ego2robot]]
- **PDF**: [[99_Attachments/papers/pdfs/ego2robot.pdf|ego2robot.pdf]]
- **项目页**: https://www-ye.github.io/ego2robot_blog/

## 研究背景

VLA 模型需要大规模、多样化的机器人演示数据，但真实机器人数据采集成本高、硬件受限、交互多样性不足。第一视角人体操作视频（egocentric human videos）场景和任务多样性丰富，但人与机器人本体差异大，直接用于训练存在 embodiment gap。已有工作在小规模或单任务上验证过 retarget-and-render 路线，但大规模预训练价值尚未被系统探索。

## 核心方法

Ego2Robot 将 egocentric 人体视频转换为机器人训练数据，分为三个阶段：

### 1. Action Alignment（动作对齐）

**Hand-to-Gripper Retargeting**
- 从 21 个手部关键点提取虚拟指尖：70% 食指尖 + 30% 中指尖
- TCP = (拇指尖 + 虚拟指尖) / 2
- 夹爪开合宽度 = 拇指尖与虚拟指尖距离
- 构建右手/左手统一的夹爪坐标系：x 接近轴、y 法向、z 夹爪轴

**Temporal Smoothing**
- Savitzky-Golay 滤波平滑位置与宽度
- Gaussian-weighted SLERP 平滑方向

**Action Speed Alignment**
- 人手动作速度显著快于机器人遥操作
- 按数据源分别降采样：ANT/EgoDex 60%、EgoVerse 45%、ViTRA 25%

### 2. Visual Alignment（视觉对齐）

- **Arm Segmentation**: SAM 3 分割人手区域
- **Hand Removal**: ProPainter 视频修复去除手臂、重建背景
- **Robot Base Pose Search**: 在轨迹质心周围网格搜索，用 MuJoCo IK 验证可行性，选出使最多关键帧可达的 base placement
- **IK and Rendering**: 逐帧求解 IK，从原相机视角渲染机器人
- **Depth-Aware Compositing**: 按深度顺序将机器人合成到修复后的场景

支持 15 种机器人形态：Panda、UR5e、ARX-L5、xArm7、Sawyer、Kinova Gen3、IIWA、Jaco、FR3、UR10e、ViperX、WidowX、Piper、YAM、Aloha-Agilex。

### 3. Quality Curation（质量筛选）

三级过滤：
- **L1 Pipeline-internal**: IK 失败、自碰撞、动作异常、工作空间覆盖不足
- **L2 Statistical**: 极值动作、不连续、无效帧比例过高
- **L3 VLM Consistency**: VLM 审核合成视频与原始操作意图的语义一致性

### 输入路径

- **Path A**: 带手部姿态标注的 ego 数据集
- **Path B**: 无标注视频，先用 WiLoR + DynHaMR 估计手部姿态；长视频用 Qwen3.5 切分为子任务

## 数据集规模

- 输入：~1,940 小时 egocentric 视频（ANT 7h、EgoDex 732h、ViTRA 249h、EgoVerse 954h）
- 输出：18,561 小时合成机器人训练数据，15 种形态
- 动作表示：camera-frame relative EEF（相机坐标系下的相对末端执行器位移），统一不同相机位姿和机器人形态

## 实验设置

- **模型**: Qwen3.5-4B 作为 VLM backbone + DiT action head
- **训练**: 8 GPUs，batch 12/GPU，lr 1e-5 → 1e-6 cosine，bf16，200K steps
- **微调**: 在 RoboTwin 50 个干净任务上 50K steps
- **评估**: 扩展 RoboTwin2.0，解耦为四个维度 12 个设置；另加 EBench 和真实机器人 ARX ACone

## 主要结果

### 混合预训练收益

| 配置 | RoboTwin Clean | RoboTwin Rand | Visual | Scene | Embody | Task | EBench Avg |
|---|---|---|---|---|---|---|---|
| Robot-only | 62.2 | 50.9 | 61.4 | 52.9 | 23.8 | 46.2 | 39.6 |
| Ego2R+Robot (1:1) | 68.1 | 53.5 | 67.3 | 56.9 | 27.2 | 54.1 | 49.8 |
| 相对提升 | +5.9 | +2.6 | +5.9 | +4.0 | +3.4 | +7.9 | +10.2 |

- **Visual appearance 受益最大**：背景 +4、光照 +8、机器人颜色 +6
- **Embodiment transfer**：ARX 44→51，UR5 20→31（3:1 时峰值）
- **Task semantics**：未见物体 +11，语言改写 +5.4
- **EBench**：3:1 比例最佳（51.7，+12.1）

### 消融实验

- 仅用原始 ego 数据：RoboTwin Rand 28.1%
- 经 Ego2Robot pipeline（单形态）：31.7%（+3.6）
- 15 形态：33.5%
- 加入原始 ego 作为第 16 个“形态”：37.3%

### 真实机器人

ARX ACone 上 5 个长程任务：
- Robot-only < Mix（Ego2R+Robot 1:1 预训练）< Mix + Ego2R Play
- Put Blocks +14，Insert Screw +13

## 个人思考与启发

1. **大规模 ego-to-robot 数据确实能补机器人数据**：优势不在轨迹覆盖，而在视觉鲁棒性、跨本体迁移和语义泛化。
2. **camera-frame relative EEF 是关键设计**：避免每视频标定和世界坐标系不兼容问题，使多源、多形态数据可统一。
3. **base placement 搜索解决了一个工程痛点**：没有真实机器人 base 时，通过 IK 可行性优化找到合理位置。
4. **解耦评估比单一 OOD 分数更有价值**：能定位收益来源，指导数据配比和 pipeline 改进。
5. **速度对齐不可忽视**：人手和机器人动作速度分布差异会直接影响训练效果。

## 局限与未来

- 只映射到平行夹爪，丢失手指精细操作
- 修复/渲染在严重遮挡或复杂光照下可能产生伪影
- 评估局限于 RoboTwin2.0 任务范围
- 未来可扩展到灵巧手、生成式渲染、更宽任务域

## 相关论文与概念

- [[04_Embodied-AI/Data-and-Evaluation/Ego-to-Robot-Synthesis|Ego-to-Robot Synthesis]] — 通用范式
- [[04_Embodied-AI/Data-and-Evaluation/Hand-to-Gripper-Retargeting|Hand-to-Gripper Retargeting]]
- [[04_Embodied-AI/Data-and-Evaluation/Camera-Frame-Relative-EEF|Camera-Frame Relative EEF]]
- [[04_Embodied-AI/Data-and-Evaluation/Robot-Data-Quality-Curation|Robot Data Quality Curation]]
- [[03_Robotics/Simulation/Disentangled-Robot-Generalization-Benchmark|Disentangled Generalization Benchmark]]
- [[h2r|h2r]] — Human-to-Robot 相关数据处理
- [[phail|phail]] — VLA benchmark
- [[pi-0-6|pi-0-6]] — VLA policy
- [[cosmos-policy|cosmos-policy]] — world model + policy
- [[characterizing-vla-models|characterizing-vla-models]] — VLA 分析
