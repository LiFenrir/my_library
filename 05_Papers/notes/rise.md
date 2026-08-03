---
title: "RISE: Self-Improving Robot Policy with Compositional World Model"
description: "基于组合世界模型的自改进机器人策略。"
tags: ["具身智能", "World Model", "Self-Improving", "Robotics", "VLA", "Reinforcement Learning", "Diffusion Model", "机器人操作"]
created: 2026-07-15
---

# RISE: Self-Improving Robot Policy with Compositional World Model

## 基本信息
- **作者**: Jiazhi Yang, Kunyang Lin, Jinwei Li, Wencong Zhang, Tianwei Lin, Longyan Wu, Zhizhong Su, Hao Zhao, Ya-Qin Zhang, Li Chen, Ping Luo, Xiangyu Yue, Hongyang Li
- **机构**: The Chinese University of Hong Kong, Kinetix AI, The University of Hong Kong, Shanghai Innovation Institute, Horizon Robotics, Tsinghua University
- **链接**: https://opendrivelab.com/kai0-rl
- **发表**: arXiv preprint, 2026
- **代码**: 即将开源 (Code and models will be released publicly)

## 研究背景与动机

### 问题陈述
- **VLA (Vision-Language-Action) 模型的局限**: 尽管 VLA 模型在大规模预训练后具备广泛的语义理解和指令跟随能力，但在接触丰富 (contact-rich) 和动态操作任务中仍然脆弱。微小的执行偏差会累积成严重失败。
- **模仿学习 (IL) 的根本缺陷**: IL 受限于专家演示的质量和覆盖范围，同时存在 exposure bias 问题——一旦机器人偏离专家流形，就缺乏恢复能力，导致错误累积。
- **物理世界 RL 的瓶颈**: 在物理世界中进行 on-policy RL 受限于安全风险、硬件成本和手动重置环境的需求。交互是串行的、耗时的、劳动密集型的。
- **World Model 的挑战**: 现有世界模型虽然视觉真实感提升，但 (1) 对多种动作的可控性 (controllability) 仍不足；(2) 需要密集的学习信号而非仅依赖二元的终端成功指示。

### 核心洞察
将机器人交互从物理环境转移到想象空间 (imaginative space)，通过构建一个组合式世界模型 (Compositional World Model) 来实现可扩展的在线策略改进。

![[99_Attachments/papers/images/rise/b74c1d6e18efcedf5c4e0d00349fab5b9648ea9ac22b3b8e21d0d81926c0cf1b.jpg]]

## 核心方法

### 1. Compositional World Model (组合式世界模型)

将世界建模分解为两个独立优化的子问题：

#### (1) Controllable Dynamics Model (可控动力学模型)
- **初始化**: 基于预训练的 Genie Envisioner (GE-base)，继承 LTX-Video 的架构优势
- **关键改进**:
  - 增加轻量级 action encoder，实现对细粒度机器人动作的精确控制
  - 对 context frames 施加更强的噪声，提高对运动模糊和视觉伪影的鲁棒性
  - **Task-Centric Batching 策略**: 每个 batch 从少量任务中采样，但覆盖同一任务下不同动作的更多样本。优先保证动作多样性而非场景多样性，显著提升动作可控性
- **效率优势**: 相比 Cosmos (生成 25 帧多视角观测需 10 分钟以上)，GE 仅需不到 2 秒，实现 **300x 加速**
- **预训练数据**: Agibot World 和 Galaxea 大规模机器人数据集

#### (2) Progress Value Model (进度价值模型)
- **初始化**: 基于预训练 VLA 策略 $\pi_{0.5}$，继承机器人-centric 理解和多视角输入兼容性
- **训练目标** (联合优化):
  - **Progress Estimate Loss** (前 10k 步):
    $$
    \mathcal{L}_{\text{prog}} = \mathbb{E}_{(o_t, \ell) \sim \mathcal{D}_{\exp}} \left[ \left(\mathcal{V}(o_t, \ell) - t/T\right)^2 \right]
    $$
    提供密集但过于平滑的信号
  - **Temporal-Difference (TD) Learning** (后 40k 步):
    $$
    \mathcal{L}_{\text{TD}} = \mathbb{E}_{(o_t, \ell, o_{t+1}) \sim \mathcal{D}} \left[ (\mathcal{V}(o_t, \ell) - y_t)^2 \right]
    $$
    $$
    y_t = r_t + \gamma \mathcal{V}(o_{t+1}, \ell)
    $$
    其中 $r_t$ 在中间步骤为 0，成功/失败回合结束时分别为 $+1/-1$。提供对细微失败的敏感性
- **最终目标**: $\mathcal{L}_{\mathcal{V}} = \mathcal{L}_{\text{prog}} + \mathcal{L}_{\text{TD}}$

### 2. Advantage 计算

对于动作块 $\mathbf{a}_t = [a_t, a_{t+1}, \ldots, a_{t+H-1}] \sim \pi(\cdot | o_t, \ell)$，动力学模型预测未来观测:

$$
\hat{o}_{t+1}, \ldots, \hat{o}_{t+H} = \mathcal{D}(\mathbf{O}_t, \mathbf{a}_t)
$$

Advantage 定义为动作块上平均累积改进:

$$
A(o_t, \mathbf{a}_t, \ell) = \left(\frac{1}{H} \sum_{k=1}^{H} \mathcal{V}(\hat{o}_{t+k}, \ell)\right) - \mathcal{V}(o_t, \ell)
$$

### 3. Policy Warm-up (策略预热)

- 在离线收集数据上微调预训练策略 $\pi_{0.5}$
- 数据组成: 专家演示 + 策略 rollout (成功/失败) + 人工干预修正 (DAgger)
- **关键设计**:
  - 仅对 rollout 数据使用学习到的 advantage 标签
  - 专家演示和人工修正数据直接分配最优 advantage (标记为 1)
  - 将 advantage 离散化为 10 个均匀区间 (bin)
- 使策略获得 advantage-conditioned 能力，为后续自改进奠基

### 4. Self-Improving Loop (自改进循环)

迭代执行两个阶段:

#### Rollout Stage
1. 从离线数据集中采样初始状态
2. 用最优 advantage (1) 提示 rollout 策略生成动作:
   $$
   \hat{\mathbf{a}}_t = \pi_{\text{rollout}}(\mathbb{1}, o_t, \ell)
   $$
3. 动力学模型合成未来 $H$ 个视觉状态
4. 价值模型评估实际 advantage $A^{\pi_{\text{rollout}}}(o_t, \hat{\mathbf{a}}_t, \ell)$
5. 想象状态也作为后续 rollout 的输入 (最多连续 2 次，防止误差累积)
6. Rollout 策略参数通过 EMA 从行为策略权重混合更新

#### Training Stage
- 在线 rollout 数据 $\langle o, \hat{a}, A \rangle$ 与离线标注数据混合
- VLA 在 advantage 条件下训练生成对应动作:
  $$
  \pi(A^{\pi_{\text{rollout}}}(o, \hat{\mathbf{a}}_t, \ell), o_t, \ell) \rightarrow \hat{\mathbf{a}}
  $$
- 使用 flow-matching 准则优化

![[99_Attachments/papers/images/rise/abe94c0c8ae4740ab365ad1746684f6cb913a27b5a92c37128e5de633cb2602d.jpg]]

## 关键创新点

1. **组合式世界模型设计**: 将动力学预测和价值估计解耦，允许各自采用最适合的架构和训练目标。动力学模型用视频扩散模型保证生成效率，价值模型用 VLA 骨干保证机器人-centric 理解。

2. **Task-Centric Batching**: 针对异构动作数据的预训练不稳定性，提出以任务为中心的批次采样策略，显著提升动作可控性和微调效率。

3. **Progress + TD 联合价值学习**: 结合进度估计的密集性和 TD 学习对失败的敏感性，解决了单一目标要么过于平滑、要么数值不稳定的问题。

4. **无需终端状态模拟的 Advantage 计算**: 不同于先前方法需要显式模拟终端状态获取奖励，RISE 直接为动作块计算 chunk-wise advantage，避免了对生成长视频可靠性的过度依赖。

5. **零推理开销**: 世界模型仅在训练阶段使用，实际部署时策略推理不依赖世界模型，计算开销为零。

## 实验结果

### 实验设置
- **硬件**: 双臂 7-DoF AgileX 机器人，绝对关节控制，30Hz 控制频率
- **输入**: 3 视角 RGB 图像 (192x256)，包括俯视和双侧腕部相机
- **任务**:
  1. **Dynamic Brick Sorting**: 从运行传送带上精确拾取彩色积木并放入对应颜色箱中
  2. **Backpack Packing**: 打开背包、放入衣物、提起、拉拉链 (涉及可变形物体)
  3. **Box Closing**: 放置杯子、折叠盖板、将卡舌塞入盒中 (需要精确双手协调)

![[99_Attachments/papers/images/rise/d213614516f5e980834581657e9f25ecaaf4fcb55b02844a23c2d4fd646c9bf5.jpg]]

### 主实验结果 (Table I)

| Method | Dynamic Brick Succ. (%) | Sorting Score | Backpack Packing Succ. (%) | Score | Box Closing Succ. (%) | Score |
|--------|------------------------|---------------|---------------------------|-------|----------------------|-------|
| $\pi_{0.5}$ | 35.00 | 8.28 | 30.00 | 4.25 | 35.00 | 7.50 |
| $\pi_{0.5}$+DAgger | 15.00 | 6.10 | 50.00 | 7.00 | 40.00 | 7.50 |
| $\pi_{0.5}$+PPO | 10.00 | 7.68 | 35.00 | 5.88 | 10.00 | 4.75 |
| $\pi_{0.5}$+DSRL | 10.00 | 6.65 | 10.00 | 3.50 | 10.00 | 7.63 |
| RECAP | 50.00 | 9.00 | 40.00 | 6.13 | 60.00 | 8.13 |
| **RISE (Ours)** | **85.00** | **9.78** | **85.00** | **9.50** | **95.00** | **9.88** |

- RISE 在所有任务上显著超越所有基线
- 相比 RECAP: Dynamic Brick Sorting **+35%**, Backpack Packing **+45%**, Box Closing **+35%**
- 在线 RL 方法 (PPO, DSRL) 表现出严重不稳定性，性能反而下降

### 消融实验

#### 离线数据比例 (Table II)
- 最优比例为 **0.6** (60% 离线 + 40% 在线)
- 比例过低 (0.1): 灾难性遗忘，成功率跌至 5%
- 比例过高 (0.9): 过度正则化，限制探索能力

#### 在线动作与状态的作用 (Table III)
- 仅离线数据: Complete Succ. 35%
- + 在线动作: Complete Succ. 40% (动作空间探索扩展)
- + 在线动作和状态: Complete Succ. **70%** (动态生成的状态提供更丰富的训练分布)

#### 模块设计消融 (Table IV)
- **Dynamics w/o Pre-train**: Sorting Acc. 下降 32.15%，验证视觉先验的重要性
- **Dynamics w/o Task-Centric**: Complete Succ. 下降 30%，验证任务中心批次的有效性
- **Value w/o Progress**: Sorting Acc. 下降约 6%，验证密集信号的重要性
- **Value w/o TD Learning**: Complete Succ. 下降 35%，验证 TD 学习对鲁棒估计的关键作用

#### 动力学模型可靠性 (Table V)
- 在 PSNR、LPIPS、SSIM、FVD、EPE 等指标上全面超越 Cosmos 和 Genie Envisioner
- EPE (光流端点误差) 显著降低，验证 Task-Centric 预训练有效增强运动感知

![[99_Attachments/papers/images/rise/4c8dff8d4bd3caa1a22b98a8e09f5c6fa5d638dab29982249bbca27d935a1425.jpg]]

## 个人思考与启发

1. **"物理成本 → 计算成本" 的范式转移**: RISE 的核心价值在于将机器人学习的主要瓶颈从物理交互转移到计算。虽然训练高保真世界模型计算成本高昂，但这比大规模物理交互更可扩展、更安全。

2. **组合优于端到端**: 将世界模型分解为动力学 + 价值两个模块，允许各自采用最优架构。这种"分而治之"的思路值得在其他复杂系统中借鉴。

3. **Task-Centric Batching 的启示**: 在异构数据预训练中，保证"同一任务下的动作多样性"比"跨任务的场景多样性"更重要。这对机器人数据集的采样策略有直接影响。

4. **Advantage 离散化的实践智慧**: 将连续 advantage 离散为 10 个 bin，既保留了排序信息，又降低了学习难度。这是一种在复杂策略优化中平衡表达能力和训练稳定性的实用技巧。

5. **离线锚定 + 在线探索的平衡**: 实验表明 0.6 的离线比例最优，这揭示了自改进系统的一个核心张力——既要保持对物理可行行为的记忆，又要给探索留出空间。

6. **局限与方向**:
   - 世界模型在罕见场景下仍可能产生物理不合理的过渡
   - 最优的虚实数据比例仍需调参，缺乏理论指导
   - 未来可探索 uncertainty-aware imagination 和显式物理约束编码

## 相关论文

- π0.5 — 基础 VLA 策略，RISE 的策略和价值模型初始化来源
- RECAP — Advantage-conditioned 离线 RL 方法，RISE warm-up 阶段的主要参考
- Genie Envisioner — RISE 动力学模型的基础架构
- Cosmos — 世界模型基线对比方法
- π0 — Flow-matching VLA 模型
- OpenVLA — 开源 VLA 模型
- Diffusion Policy — 动作扩散策略
- Agibot World — 动力学模型预训练数据集
- Galaxea — 动力学模型预训练数据集
- Dream to Manipulate — 组合式世界模型用于机器人模仿学习
- Video Language Planning — 视频语言规划
- WorldModelBench — 世界模型评测基准


## 原文

[[05_Papers/articles/rise|rise]]
