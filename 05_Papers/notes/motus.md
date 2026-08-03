---
title: "Motus: A Unified Latent Action World Model"
description: "统一的潜在动作世界模型，用 MoT 架构实现跨机器人本体的迁移。"
tags: ["世界模型", "统一模型", "潜在动作", "MoT", "光流", "跨本体迁移", "清华大学"]
created: 2026-07-15
---

# Motus: A Unified Latent Action World Model

## 基本信息

- **作者**: Hongzhe Bi*, Hengkai Tan*, Shenghao Xie*, Zeyuan Wang*, Shuhe Huang*, Haitian Liu*, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, Jun Zhu
- **机构**: 清华大学, 北京大学, 地平线机器人
- **链接**: https://arxiv.org/abs/2512.13030
- **项目页**: https://motus-robotics.github.io/motus
- **发表**: arXiv 2025

## 研究背景与动机

### 现有方法的碎片化
当前具身智能方法将认知功能分割为孤立模型：

| 模型类型 | 分布 | 功能 |
|---------|------|------|
| **VLA** | $p(a_{t+1:t+k} \mid o_t, \ell)$ | 从视觉和语言学习静态策略 |
| **World Model** | $p(o_{t+1:t+k} \mid o_t, a_{t+1:t+k})$ | 预测未来状态 |
| **IDM** | $p(a_{t+1:t+k} \mid o_{t:t+k})$ | 从视觉转换推断动作 |
| **VGM** | $p(o_{t+1:t+k} \mid o_t, \ell)$ | 生成未来视频 |
| **Video-Action Joint** | $p(o_{t+1:t+k}, a_{t+1:t+k} \mid o_t, \ell)$ | 联合预测视频和动作 |

这种碎片化阻碍了多模态生成能力的统一，也限制了从大规模异构数据中学习。

### 两大核心挑战

**挑战 1: 统一多模态生成能力**
- 如何在单一框架内联合建模视觉、语言和动作的多种分布
- 现有 UWM 等方法通常从头训练或基于小模型，缺乏 VLM 的视觉理解先验或 VGM 的物理交互先验

**挑战 2: 利用大规模异构数据**
- 动作空间在不同本体之间差异巨大（维度、范围、语义）
- 大多数视频数据缺乏动作标注
- 无法将互联网视频/人类视频与机器人轨迹统一预训练

## 核心方法

### 1. Motus 架构: 三专家 MoT

![[99_Attachments/papers/images/motus/motus_fig1_architecture.jpg]]

**Mixture-of-Transformers (MoT) 架构**，集成三个专家：

| 专家 | 基础模型 | 功能 |
|------|---------|------|
| **生成专家 (VGM)** | Wan 2.2 5B | 视频生成 |
| **理解专家 (VLM)** | Qwen3-VL-2B | 3D 定位、空间理解、物体定位 |
| **动作专家** | 自定义 Transformer | 动作预测 |

**三模型联合注意力 (Tri-model Joint Attention)**:
- 每个专家保持独立的 Transformer 模块
- 多头自注意力层**共享拼接**
- 保留专家的专业功能，同时实现跨模态特征融合

**训练目标** (修正流):
$$l^\theta_{\text{action}} = \mathbb{E}\|v^\theta_a - (\epsilon_a - a_{t+1:t+k})\|^2_2$$
$$l^\theta_{\text{obs}} = \mathbb{E}\|v^\theta_o - (\epsilon_o - O_{t+1:t+k})\|^2_2$$

**UniDiffuser 风格调度器**: 为视频和动作分配不同时间步和噪声尺度，支持灵活切换推理模式。

### 2. 动作密集-视频稀疏预测

![[99_Attachments/papers/images/motus/motus_fig2_dense_sparse.jpg]]

**问题**: 动作块预测导致视频 token 数量远超动作 token，模型过拟合于视频预测。

**解决方案**: 视频帧下采样至动作帧率的 1/6，保持视频和动作 token 数量平衡。

### 3. 潜在动作 (Latent Actions)

![[99_Attachments/papers/images/motus/motus_fig3_latent_vae.jpg]]

**核心洞察**: 利用光流作为通用运动表示，编码像素级"增量动作"。

**实现流程**:
1. 用 DPFlow 计算连续帧间的光流
2. 光流转为 RGB 图像
3. DC-AE 深度卷积自编码器压缩为 4×512 维 token
4. 轻量编码器投影为 **14 维向量**（与典型机器人动作空间匹配）

**训练数据混合**:
- 90% 无标签数据（自监督重建）
- 10% 标注轨迹（弱动作监督）
  - 任务无关数据（Curobo 随机采样目标机器人动作空间）
  - 标准机器人演示

**损失函数**:
$$\mathcal{L} = \mathcal{L}_{\text{recon}} + \lambda_a \|a_{\text{real}} - a_{\text{pred}}\|^2 + \beta \mathcal{L}_{\text{KL}}$$

**意义**: 潜在动作桥接了视觉动力学与控制信号，使动作专家能从无标签视频中预训练。

### 4. 三阶段训练 + 六层数据金字塔

![[99_Attachments/papers/images/motus/motus_fig4_data_pyramid.jpg]]

**数据金字塔**（从底层到顶层，数量递减但质量递增）:

| 层级 | 数据类型 | 模态 |
|------|---------|------|
| **Level 1** | Web 数据 | 语言 + 图像 |
| **Level 2** | 第一人称人类视频 | 语言 + 图像 |
| **Level 3** | 仿真数据 | 语言 + 图像 + 动作 |
| **Level 4** | 任务无关数据 | 图像 + 动作 |
| **Level 5** | 多机器人任务轨迹 | 语言 + 图像 + 动作 |
| **Level 6** | 目标机器人任务轨迹 | 语言 + 图像 + 动作 |

**三阶段训练**:

| 阶段 | 目标 | 数据 | 训练内容 |
|------|------|------|---------|
| **Stage 1** | 学习视觉动力学 | Level 2, 3, 5 | 仅 VGM |
| **Stage 2** | 学习动作表示 | Level 2, 3, 4, 5 | Motus 全模型 + 潜在动作 (VLM 冻结) |
| **Stage 3** | 目标机器人特化 | Level 6 | Motus 全模型 + 真实动作 |

## 实验结果

### 仿真: RoboTwin 2.0 (50 任务，多任务训练)

| 方法 | Clean | Randomized |
|------|-------|-----------|
| π₀.₅ | 42.98% | 43.84% |
| X-VLA | 72.80% | 72.84% |
| w/o Pretrain | 72.8% | 77.00% |
| Stage 1 only | 82.86% | 81.86% |
| **Motus** | **88.66%** | **87.02%** |

- **相比 π₀.₅: +45%** 绝对提升
- **相比 X-VLA: +15%** 绝对提升
- 多任务联合训练，仅 40K 微调步数

### 真实世界: 双臂机器人任务

在两种平台上评估（AC-One 和 Agilex-Aloha-2），涵盖：
- 空间理解
- 可变形物体操作
- 精度流体控制
- 视觉理解
- 长程规划

![[99_Attachments/papers/images/motus/motus_fig5_tasks_a.jpg]]
![[99_Attachments/papers/images/motus/motus_fig5_tasks_b.jpg]]
![[99_Attachments/papers/images/motus/motus_fig5_tasks_c.jpg]]

**AC-One 平台结果**:

| 任务 | π₀.₅ | w/o Pretrain | Motus |
|------|------|---------------|-------|
| Fold Towel | 4% | 1% | **14.5%** |
| Brew Coffee | 0% | 0% | **62%** |
| Get Water | 30% | 8% | **36%** |
| Place Cube into Plate | 46% | 60% | **100%** |
| Place Cube (OOD) | 28.1% | 18.8% | **75%** |
| Grind Coffee Beans | 8% | 0% | **92%** |
| Pour Water to Flowers | 5% | 5% | **65%** |
| Touch Keyboard | 0% | 100% | **82.5%** |
| Put Bread into Oven | 12% | 40% | **42%** |
| **Average** | **14.79%** | **25.86%** | **63.22%** |

**Agilex-Aloha-2 平台结果**:

| 任务 | π₀.₅ | w/o Pretrain | Motus |
|------|------|---------------|-------|
| Fold Towel | 27.5% | 0% | **39%** |
| Get Water | 62% | 8% | **96%** |
| Pour Water | 45% | 40% | **47.5%** |
| Touch Keyboard | 72.5% | 85% | **80%** |
| Put Bread into Oven | 36% | 0% | **34%** |
| **Average** | **48.60%** | **26.60%** | **59.30%** |

- **相比 π₀.₅: +11~48%** 提升
- 每个任务仅用 100 次演示训练

### 消融实验

![[99_Attachments/papers/images/motus/motus_fig6_ablation_a.jpg]]
![[99_Attachments/papers/images/motus/motus_fig6_ablation_b.jpg]]

| 变体 | RoboTwin Randomized |
|------|-------------------|
| w/o Pretrain | 77.00% |
| Stage 1 only | 81.86% |
| **Motus (Stage 2)** | **87.02%** |

- 三阶段训练逐步提升性能
- Stage 2（统一训练 + 潜在动作）是关键提升点

## 与 WAM 四部曲的对比

| 特性 | DreamZero | LingBot-VA | Cosmos Policy | **Motus** |
|------|-----------|------------|---------------|-----------|
| **机构** | NVIDIA | Robbyant | NVIDIA+Stanford | **清华+北大+地平线** |
| **骨干** | Wan2.1 14B | Wan2.2 5B | Cosmos-Predict2 2B | **Wan2.2 5B + Qwen3-VL 2B** |
| **架构** | 自回归 DiT | MoT 双流失散 | 零修改视频模型 | **MoT 三专家** |
| **统一性** | 视频+动作联合 | 视频+动作联合 | 视频+动作+价值 | **VLA+WM+IDM+VGM+联合** |
| **动作表示** | 真实动作 | 真实动作 | 真实动作 | **光流潜在动作** |
| **跨本体** | 视频迁移 | 无显式 | 无显式 | **光流对齐** |
| **规划** | 无 | 无 | Best-of-N | 无 |
| **核心优势** | 零样本泛化 | 长程记忆 | 极简+规划 | **统一五范式+跨本体** |

**Motus 的独特之处**:
1. **最全面的统一**: 同时集成 VLA、WM、IDM、VGM、Video-Action Joint 五种范式
2. **光流潜在动作**: 首次用光流作为跨本体通用运动表示
3. **三专家 MoT**: VGM + VLM + 动作专家，各司其职又协同
4. **六层数据金字塔**: 系统性地组织从网络到目标机器人的异构数据

## 关键洞察

1. **统一建模优于孤立模型**: 五种范式共享参数和注意力，知识互补
2. **光流是理想的跨本体桥梁**: 像素级位移天然 embodiment-agnostic
3. **潜在动作解决标注稀缺**: 90% 无标签 + 10% 弱监督即可学习可执行控制
4. **渐进式训练关键**: 从视觉动力学 → 动作表示 → 本体特化，逐步聚焦

## 局限性与未来工作

1. **推理模式切换**: 当前需手动选择推理模式，未来可探索自动切换
2. **规划能力**: 未显式集成基于价值的规划（如 Cosmos Policy 的 Best-of-N）
3. **光流计算开销**: DPFlow 计算增加预处理成本
4. **规模扩展**: 当前 5B+2B，探索更大规模统一模型

## 个人评价

**重要性**: ★★★★★
- 提出了最全面的统一框架，将五种主流范式集成到单一模型
- 光流潜在动作是跨本体学习的创新解决方案
- 在仿真和真实世界都取得 SOTA，且提升幅度显著 (+11~45%)
- 三阶段训练 + 六层数据金字塔提供了可复用的系统性方法

**与 WAM 趋势的关系**:
2025 年初 WAM 方向形成四大支柱：
- **DreamZero**: 零样本泛化 + 跨本体迁移
- **LingBot-VA**: 因果自回归 + 长程记忆
- **Cosmos Policy**: 极简适配 + 显式规划
- **Motus**: 统一五范式 + 光流跨本体

四者从不同角度验证了：**视频世界模型是机器人学习的强大基础**，且统一建模优于碎片化方法。

**可改进方向**:
- 结合 Motus 的统一框架 + Cosmos Policy 的规划能力
- 探索更高效的潜在动作编码（替代光流）
- 自动推理模式切换机制

## 相关论文

- [DreamZero](https://arxiv.org/abs/2602.15922) - NVIDIA WAM
- [LingBot-VA](https://arxiv.org/abs/2601.21998) - 因果自回归 WAM
- [Cosmos Policy](https://arxiv.org/abs/2601.16163) - 视频模型微调策略
- [UWM](https://arxiv.org/abs/2504.02792) - 统一世界模型
- [F1](https://arxiv.org/abs/2509.06951) - 桥接理解与生成到动作
- [RDT-1B](https://arxiv.org/abs/2410.07864) - 双臂操作扩散基础模型
- [AgiBot World](https://arxiv.org/abs/2503.06669) - 大规模操作平台


## 原文

[[05_Papers/articles/motus|motus]]
