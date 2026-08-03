---
title: "Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning"
description: "零架构修改地将视频生成模型单阶段微分为机器人策略、世界模型与价值函数。"
tags: ["世界模型", "视频扩散", "机器人策略", "模型预测控制", "价值函数", "NVIDIA", "Stanford"]
created: 2026-07-15
---

# Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning

## 基本信息

- **作者**: Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, Jinwei Gu
- **机构**: NVIDIA, Stanford University
- **链接**: https://arxiv.org/abs/2601.16163
- **项目页**: https://research.nvidia.com/labs/dir/cosmos-policy/
- **代码/模型/数据**: 已开源
- **发表**: arXiv 2025

## 研究背景与动机

### VLA vs 视频模型的先验差异

| 特性 | VLA (Vision-Language-Action) | 视频生成模型 |
|------|------------------------------|-------------|
| **预训练数据** | 静态图像-文本对 | 数百万视频 |
| **学习到的知识** | 语义概念 | 时间因果性、隐式物理、运动模式 |
| **对机器人的价值** | 语义泛化 | 时空动力学、物理交互理解 |

**核心假设**: 视频模型学习到的时空先验为低级控制策略提供了强大的基础。

### 现有视频模型适配方法的局限
1. **多阶段训练**: 视频微调 → 动作模块训练，引入复杂性
2. **新架构组件**: 单独的动作扩散器或逆动力学模型
3. **统一模型但未利用预训练**: 如 UVA、UWM 等自定义设计，无法充分利用时空先验

### Cosmos Policy 的核心思想
**单阶段微调**，**零架构修改**，直接将视频模型适配为机器人策略。

## 核心方法

### 骨干模型
**Cosmos-Predict2-2B-Video2World** (NVIDIA, 2025)
- 潜在视频扩散模型
- Wan2.1 时空 VAE tokenizer
- EDM 去噪分数匹配公式
- 输入: 起始图像 + 文本描述 → 输出: 后续帧序列

### 关键创新: 潜在帧注入 (Latent Frame Injection)

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig1_overview.jpg]]

**核心洞察**: 将新模态（动作、本体感受、价值）编码为潜在帧，直接注入视频模型的潜在扩散序列。

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig2_latent_injection.jpg]]

**示例序列**（双第三人称相机 + 腕部相机）:
1. 空白占位符
2. 机器人本体感受（如末端执行器位姿/关节角）
3. 腕部相机图像
4. 第一第三人称相机图像
5. 第二第三人称相机图像
6. **动作块**
7. **未来机器人本体感受**
8. **未来腕部相机图像**
9. **未来第一第三人称相机图像**
10. **未来第二第三人称相机图像**
11. **未来状态价值**

**编码方式**: 将低维向量归一化到 $[-1, +1]$ 后复制填充到 $H' \times W' \times C'$ 的潜在体积。

**序列语义**: $(\bar{s}, a, s', \bar{V}(s'))$ — 支持自左向右自回归解码。

### 联合训练目标

**训练批次构成**:
- 50% 演示数据 → 训练策略 $p(a, \bar{s'}, V(s') | s)$
- 25% 推出数据 → 训练世界模型 $p(s', V(s') | s, a)$
- 25% 推出数据 → 训练价值函数 $p(V(s') | s, a, \bar{s'})$

**条件掩码机制**: 通过控制潜在扩散序列中哪些部分作为条件、哪些作为生成目标，实现三种功能的灵活切换。

### 推理模式

**并行解码**（直接策略）:
- 同时生成动作、未来状态、价值
- 速度快，仅需动作即可执行

**自回归解码**（规划模式）:
- 顺序生成：动作 → 未来状态 → 价值
- 预测质量更高，支持分离检查点

### 基于模型的规划

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig7_planning.jpg]]

**Best-of-N 采样**:
1. 从策略采样多个动作候选
2. 用规划模型预测每个候选的未来状态和价值
3. 选择预测价值最高的动作执行

**集成策略**（提高鲁棒性）:
- 每个动作查询世界模型 3 次
- 每个未来状态查询价值函数 5 次
- 共 15 个价值预测
- **多数均值**: 确定多数预测成功/失败，取多数组的平均值

**双模型部署**:
- **策略模型**: 原始 Cosmos Policy 检查点，生成动作候选
- **规划模型**: 在推出数据上微调的检查点，提供更准确的世界模型和价值预测

### 从推出经验学习

**问题**: 仅演示数据训练的世界模型和价值函数只看到成功结果，分布狭窄。

**解决方案**:
1. 收集策略推出数据（包括失败案例）
2. 微调检查点，重加权:
   - 90% 批次: 世界模型 + 价值函数训练（各半）
   - 10% 批次: 策略训练

### 噪声分布调整

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig9_noise.jpg]]

**原始 Cosmos-Predict2**: 对数正态分布，侧重低噪声水平

**Cosmos Policy**: 混合对数正态-均匀分布，增加高噪声水平权重

**原因**: 动作生成需要高精度，高噪声区域的准确去噪至关重要。

## 实验结果

### LIBERO 仿真基准

| 方法 | Spatial | Object | Goal | Long | Average |
|------|---------|--------|------|------|---------|
| Diffusion Policy | 78.3% | 92.5% | 68.3% | 50.5% | 72.4% |
| π₀ | 96.8% | 98.8% | 95.8% | 85.2% | 94.2% |
| π₀.₅ | 98.8% | 98.2% | 98.0% | 92.4% | 96.9% |
| OpenVLA-OFT | 97.6% | 98.4% | 97.9% | 94.5% | 97.1% |
| CogVLA | 98.6% | 98.8% | 96.6% | 95.4% | 97.4% |
| **Cosmos Policy** | **98.1%** | **100.0%** | **98.2%** | **97.6%** | **98.5%** |

- **平均成功率 98.5%**，超越所有 VLA 和扩散策略
- 仅用 500 次演示训练

### RoboCasa 仿真基准

| 方法 | 每任务训练演示 | 平均成功率 |
|------|---------------|-----------|
| GR00T-N1 | 300 | 49.6% |
| UVA | 50 | 50.0% |
| DP-VLA | 3000 | 57.3% |
| π₀ | 300 | 62.5% |
| GR00T-N1.5 | 300 | 64.1% |
| Video Policy | 300 | 66.0% |
| FLARE | 300 | 66.4% |
| **Cosmos Policy** | **50** | **67.1%** |

- **SOTA 67.1%**，但仅需 **50 次演示**（其他方法需 300+）
- 数据效率显著优于所有基线

### 真实世界 ALOHA 机器人

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig3_aloha.jpg]]
![[99_Attachments/papers/images/cosmos-policy/cosmos_fig4_results.jpg]]

四个具有挑战性的双臂操作任务：
1. **put X on plate** (80 demos): 语言跟随
2. **fold shirt** (15 demos): 长程接触丰富操作
3. **put candies in bowl** (45 demos): 多模态抓取序列
4. **put candy in ziploc bag** (45 demos): 毫米级精度操作

**结果**: Cosmos Policy 获得 **最高总体分数 (93.6%)**，在 4 个任务中的 3 个上超越所有方法。

**VLA 失败模式**:

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig5_failure_a.jpg]]
![[99_Attachments/papers/images/cosmos-policy/cosmos_fig5_failure_b.jpg]]

- π₀.₅: 难以执行高精度抓取（拉链袋滑块）
- OpenVLA-OFT+: 在多模态任务中（捡糖果）动作分布建模不准确，经常在两颗糖果之间抓取

### 消融实验

| 变体 | LIBERO 平均成功率 |
|------|------------------|
| 完整 Cosmos Policy | 98.5% |
| 无辅助损失 | 97.0% (-1.5%) |
| 从头训练 | 94.6% (-3.9%) |

- 辅助损失（联合预测未来状态和价值）重要
- 视频模型预训练先验至关重要

### 基于模型的规划效果

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig7_planning.jpg]]

在两个最具挑战性的 ALOHA 任务上：
- 基础 Cosmos Policy: 基线性能
- **模型规划 (V(s'))**: **+12.5 分** 平均提升
- 模型规划优于无模型规划 (Q(s,a))

**原因分析**:
- 规划模型在推出数据上微调后，能更准确预测未来状态
- 避免基础策略的错误（如丢失拉链袋滑块抓握）

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig5_failure_b.jpg]]

## 关键设计细节

### 潜在注入实现

![[99_Attachments/papers/images/cosmos-policy/cosmos_fig8_detailed.jpg]]

**详细流程**:
1. 构造图像序列（含空白占位符图像）
2. VAE tokenizer 编码为潜在帧
3. 用归一化并复制的模态数据覆盖占位符潜在帧
4. 添加高斯噪声（按噪声水平缩放）
5. 训练模型去噪损坏部分

**提取动作**: 对潜在体积中的所有副本取平均，反归一化到原始尺度。
**提取价值**: 标量，对整个潜在体积取平均后反归一化。

### 训练配置

- **预训练模型**: Cosmos-Predict2-2B
- **VAE**: Wan2.1，压缩比 $4 \times 16 \times 16$
- **优化器**: AdamW
- **批次**: 50% 演示 + 50% 推出（各半分世界模型和价值函数）
- **动作表示**: 末端执行器位姿 (7D) + 关节角 (7D) + 夹爪 (1D) × 2臂 = 30D

## 与相关工作的关系

### 与 DreamZero / LingBot-VA 的对比

| 特性 | DreamZero | LingBot-VA | Cosmos Policy |
|------|-----------|------------|---------------|
| **机构** | NVIDIA | Robbyant | NVIDIA + Stanford |
| **骨干** | Wan2.1-I2V-14B | Wan2.2-5B | Cosmos-Predict2-2B |
| **参数** | 14B | 5.3B | 2B |
| **架构修改** | 添加状态/动作编码器 | MoT 双流失散 | **零修改** |
| **动作生成** | 联合去噪 | 视频先预测，动作后解码 | 潜在帧注入 |
| **规划能力** | 无显式规划 | 无显式规划 | **Best-of-N + 价值函数** |
| **推出学习** | 无 | 无 | **有，用于精炼世界模型** |
| **核心优势** | 零样本泛化 | 长程记忆、样本效率 | 简单性、数据效率、规划 |

**Cosmos Policy 的独特之处**:
1. **极简主义**: 零架构修改，单阶段微调
2. **统一框架**: 策略、世界模型、价值函数共享同一架构
3. **显式规划**: 通过价值函数实现模型预测控制
4. **从推出学习**: 利用策略推出数据持续改进

## 局限性与未来工作

1. **推理速度**: 模型规划约 5 秒/动作块，限制动态任务适用性
2. **推出数据需求**: 有效规划需要大量推出数据
3. **搜索深度**: 当前仅一层搜索树，扩展预测范围可能更有效
4. **历史使用**: 当前仅使用当前时刻观测，未利用历史上下文

## 个人评价

**重要性**: ★★★★★
- 提出了最简洁的视频模型适配方法（零架构修改）
- 在多个基准上达到 SOTA，数据效率极高（50 演示 vs 300+）
- 首次展示了从视频模型微调的统一策略-世界模型-价值函数框架
- 完全开源，利于社区复现

**核心洞察**:
1. **视频模型的学习能力可直接迁移到动作生成**: 无需特殊架构，视频扩散的学习算法本身就能建模复杂的多模态分布
2. **潜在帧注入是通用机制**: 可扩展至任何新模态（力觉、触觉等）
3. **辅助监督提升策略性能**: 联合预测未来状态和价值不仅支持规划，也改善策略本身

**与 WAM 趋势的关系**:
Cosmos Policy、DreamZero、LingBot-VA 三篇论文共同构成了 2025 年初 WAM (World Action Model) 方向的三大支柱：
- **Cosmos Policy**: 极简适配 + 显式规划
- **DreamZero**: 大规模零样本泛化 + 跨本体迁移
- **LingBot-VA**: 因果自回归 + 长程记忆

三者都验证了：**预训练视频模型 → 机器人策略** 是一条可行且强大的路径。

## 相关论文

- [DreamZero](https://arxiv.org/abs/2602.15922) - NVIDIA WAM 工作
- [LingBot-VA](https://arxiv.org/abs/2601.21998) - 因果自回归 WAM
- [π₀](https://arxiv.org/abs/2410.24164) / [π₀.₅](https://arxiv.org/abs/2504.16054) - VLA baseline
- [OpenVLA](https://arxiv.org/abs/2406.09246) - 开源 VLA
- [Cosmos](https://arxiv.org/abs/2501.03575) - NVIDIA 世界基础模型平台
- [UVA](https://arxiv.org/abs/2503.00200) - 统一视频动作模型
- [FLARE](https://arxiv.org/abs/2505.15659) - 隐式世界建模机器人学习


## 原文

[[05_Papers/articles/cosmos-policy|cosmos-policy]]
