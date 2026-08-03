---
title: "πRL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models"
description: "基于 Flow Matching 的 VLA 在线 RL 微调方法。"
tags: ["VLA", "RL", "Flow Matching", "Robotics", "PPO", "π0", "π0.5", "Sim-to-Real"]
created: 2026-07-15
---

# πRL: Online RL Fine-tuning for Flow-based Vision-Language-Action Models

## 基本信息
- **作者**: Kang Chen, Zhihao Liu, Tonghe Zhang, Zhen Guo, Si Xu, Hao Lin, Hongzhi Zang, Xiang Li, Bingwen Wei, Jiakai Zhou, Quanlu Zhang, Zhaofei Yu, Guoliang Fan, Tiejun Huang, Yu Wang, Chao Yu
- **机构**: Tsinghua University, Peking University, Institute of Automation (CAS), Carnegie Mellon University, Infinigence AI, Zhongguancun Academy
- **链接**: [GitHub](https://github.com/RLinf/RLinf) / [HuggingFace](https://huggingface.co/RLinf)
- **发表**: arXiv preprint, 2025

## 研究背景与动机
Vision-Language-Action (VLA) 模型已成为通用机器人的主流方案，能够将高层多模态推理与底层物理控制相结合。当前 VLA 的训练遵循预训练 + 监督微调 (SFT) 的范式，但依赖大规模、高质量的专家轨迹数据，收集成本高昂且费力。此外，SFT 得到的模型容易过拟合到专家演示上，性能受限于演示数据的质量。

近期研究开始探索用强化学习 (RL) 扩展 VLA 的训练流程，形成预训练 → SFT → RL 的新范式。然而，现有的 VLA-RL 方法主要针对自回归 VLA（如 OpenVLA、OpenVLA-OFT），这些方法通过离散或并行的动作解码器生成输出。与之相对，基于 Flow Matching 的 VLA（如 π0、π0.5）通过迭代细化生成动作，在高频动作块生成和高度灵巧任务上具有优势，但现有的 RL 算法无法直接应用于这类模型。

核心挑战在于：**Flow Matching 的确定性 ODE 采样过程使得动作的对数似然 (log-likelihood) 难以精确计算**，同时缺乏探索能力。本文提出 πRL 框架，通过 Flow-Noise 和 Flow-SDE 两种技术路径解决这一难题，使基于 Flow 的 VLA 能够进行在线 RL 微调。

## 核心方法

### 问题定义
将任务建模为马尔可夫决策过程 (MDP) $\mathcal{M} = (\mathcal{S}, \mathcal{A}, P_0, P_{\mathrm{ENV}}, R_{\mathrm{ENV}}, \gamma)$，目标是学习策略 $\pi_\theta$ 最大化期望折扣回报：

$$
\mathcal{J}(\pi_\theta) = \mathbb{E}_{\pi_\theta, P_0} \left[ \sum_{t=0}^{T} \gamma^t R_{\mathrm{ENV}}(s_t, a_t) \right]
$$

策略梯度通过采样轨迹近似：

$$
\nabla_\theta \mathcal{J}(\pi_\theta) = \mathbb{E}_{\pi_\theta, P_0} \left[ \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t \mid s_t) A(s_t, a_t) \right]
$$

对于基于 Flow 的 VLA，模型学习条件向量场 $\mathbf{v}_\theta$，通过最小化 Conditional Flow Matching (CFM) 损失将标准高斯噪声分布转换为目标动作分布：

$$
\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{\tau, p(\mathbf{A}_t, \mathbf{o}_t), q(\mathbf{A}_t^\tau \mid \mathbf{A}_t)} \left[ \| \mathbf{v}_\theta(\mathbf{A}_t^\tau, \mathbf{o}_t) - \mathbf{u}(\mathbf{A}_t^\tau \mid \mathbf{A}_t) \|_2^2 \right]
$$

其中条件概率路径为 $\mathbf{A}_t^\tau = \tau \mathbf{A}_t + (1-\tau)\epsilon$，$\epsilon \sim \mathcal{N}(0, I)$，对应的真实向量场为 $\mathbf{u}(\mathbf{A}_t^\tau \mid \mathbf{A}_t) = \mathbf{A}_t - \epsilon$。

![[99_Attachments/papers/images/pirl/015e721ec9a53a4fdc041806d12d19dad9fbc868134c8ad973a4bf47b0edc606.jpg]]

### Flow-Noise 方法
Flow-Noise 受 ReinFlow 启发，将去噪过程建模为离散时间 MDP，通过引入可学习的噪声网络实现精确的对数似然计算。

**随机性注入**：将噪声幅度参数化为神经网络，在去噪过程中动态学习。单步转移建模为高斯分布 $p(\mathbf{A}^{\tau+\delta} \mid \mathbf{A}^\tau) \sim \mathcal{N}(\mu_\tau, \Sigma_\tau)$：

$$
\begin{cases}
\mu_\tau = \mathbf{A}^\tau + \mathbf{v}^\tau \cdot \delta \\
\Sigma_\tau = \mathrm{diag}(\sigma_{\theta'}^2)
\end{cases}
$$

其中 $\sigma_{\theta'}(\cdot)$ 是从噪声注入网络学习的标准差，以动作 $\mathbf{A}^\tau$ 和观察 $\mathbf{o}$ 为条件。噪声网络与速度场联合训练，但在推理时丢弃，保留确定性策略。

**对数似然估计**：将推理过程离散化为 $K$ 个均匀步骤，定义时间点序列 $\{\tau_0, \tau_1, \dots, \tau_K\}$，其中 $\delta = 1/K$，$\tau_k = k \cdot \delta$。整个去噪序列 $\mathcal{A} = (\mathbf{A}^0, \dots, \mathbf{A}^1)$ 的精确对数概率为：

$$
\log \pi(\mathcal{A} \mid \mathbf{o}) = \log \left( \pi(\mathbf{A}^0 \mid \mathbf{o}) \prod_{k=0}^{K-1} \pi(\mathbf{A}^{\tau_{k+1}} \mid \mathbf{A}^{\tau_k}, \mathbf{o}) \right)
$$

这使得 Flow-based 策略优化可以在标准 MDP 框架内进行。

![[99_Attachments/papers/images/pirl/4c63687e4d259c4d7ba1748e4c6158b039652053af1e6c0a49ad7523349fe11a.jpg]]

![[99_Attachments/papers/images/pirl/01c4ca2085138e207691809d1a2bf7923a180041d7d4b6709fa99ee8a4987bbb.jpg]]

### Flow-SDE 方法
Flow-SDE 受 Flow-GRPO 启发，通过将 ODE 转换为等价的 SDE 来增强随机探索，并构建双层 MDP 耦合去噪过程与策略-环境交互。

**ODE 到 SDE 的转换**：确定性 ODE 采样轨迹由前向欧拉方法描述：

$$
d\mathbf{A}^\tau = \mathbf{v}^\tau d\tau
$$

基于概率流 ODE 与 SDE 的联系，将其转换为等价 SDE：

$$
d\mathbf{A}^\tau = \underbrace{\left(\mathbf{v}^\tau - \frac{1}{2} g^2(\tau) \nabla \log q_\tau(\mathbf{A}^\tau)\right) d\tau}_{\text{Drift Term}} + \underbrace{g(\tau) d\mathbf{w}}_{\text{Diffusion Term}}
$$

其中 $g(\tau)$ 是控制噪声调度的标量函数，$\nabla \log q_\tau(\mathbf{A}^\tau)$ 是边缘分布的 score 函数。利用 score 函数与速度场的关系 $\nabla \log q_\tau(\mathbf{A}^\tau) = -\frac{\mathbf{A}^\tau}{\tau} - \frac{1-\tau}{\tau} \mathbf{v}^\tau$，并设置噪声调度 $\sigma_\tau = a\sqrt{\frac{\tau}{1-\tau}}$，得到最终的 SDE 形式：

$$
d\mathbf{A}^\tau = \left[ \mathbf{v}^\tau + \frac{\sigma_\tau^2}{2\tau} \left(\mathbf{A}^\tau + (1-\tau)\mathbf{v}^\tau\right) \right] d\tau + \sigma_\tau d\mathbf{w}_\tau
$$

离散化后，转移概率 $p(\mathbf{A}^{\tau+\delta} \mid \mathbf{A}^\tau) \sim \mathcal{N}(\mu_\tau, \Sigma_\tau)$ 为各向同性高斯分布：

$$
\begin{cases}
\mu_\tau = \mathbf{A}^\tau + \left[ \mathbf{v}^\tau + \frac{\sigma_\tau^2}{2\tau}(\mathbf{A}^\tau + (1-\tau)\mathbf{v}^\tau) \right] \cdot \delta \\
\Sigma_\tau = \sigma_\tau^2 \delta \cdot \mathbf{I}
\end{cases}
$$

![[99_Attachments/papers/images/pirl/03473c3458a5c43ab41130bf12c5f82a4033739b1e7c49be6cfbe322227f4117.jpg]]

**双层 MDP 形式化**：
- **状态** $\bar{s}_t^\tau = (\mathbf{o}_t, \mathbf{A}_t^\tau)$：观察与动作状态的元组
- **动作** $\bar{a}_t^\tau$：内层循环的下一步去噪动作，外层循环的执行动作
- **转移** $\bar{P}(\bar{s}_{t'}^{\tau'} \mid \bar{s}_t^\tau, \bar{a}_t^\tau)$：$\tau < 1$ 时进行内层去噪转移，$\tau = 1$ 时与环境交互并重置动作状态
- **奖励** $\bar{R}(\bar{s}_t^\tau, \bar{a}_t^\tau)$：仅在去噪完成并与环境交互时获得环境奖励

![[99_Attachments/papers/images/pirl/08504e777fbe96595a461f1f214a47ac3604d28ddbc0b3aebec214cb6fbead1b.jpg]]

**混合 ODE-SDE 采样**：为降低计算成本，采用混合策略：在每个步骤随机采样一个去噪时间 $\tau_t$ 进行随机 SDE 探索，其余去噪步骤作为确定性 ODE 更新。这有效缩短了 MDP 时间范围，同时保持与原始双层框架的理论一致性。

![[99_Attachments/papers/images/pirl/027046c724609c5a46a3bd11ddc0a083feab303e5d879297349bec1cd4e8945d.jpg]]

### 整体训练流程

**策略优化 (PPO)**：采用近端策略优化 (PPO) 进行策略更新，使用广义优势估计 (GAE)：

$$
\hat{A}_t = \sum_{k=0}^{T-t} (\gamma\lambda)^k \mathcal{T}_{t+k}
$$

PPO 目标函数为：

$$
\mathcal{J}(\pi_\theta) = \mathbb{E}_t \left[ \min\left(\rho_t(\theta)\hat{A}_t, \mathrm{clip}(\rho_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right) \right]
$$

概率比 $\rho_t(\theta)$ 根据 Flow-Noise 或 Flow-SDE 的形式分别计算。

**Critic 设计**：采用共享的 actor-critic 架构。对于 π0.5，critic 直接连接在 VLM 输出后；对于 π0，由于动作专家需要噪声动作和状态作为输入，通过对整个去噪轨迹上的价值估计取平均来近似：

$$
V_{\mathrm{expert}}(\mathbf{o}_t) \approx \mathbb{E}_{\tau \sim U[0,1]} \left[ V_{\mathrm{expert}}(\mathbf{o}_t, \mathbf{A}_t^\tau) \right]
$$

![[99_Attachments/papers/images/pirl/d398ae79b7898279a8b28e28ba4dd0118f7bec6489afb4271e7d9816468948cd.jpg]]

## 关键创新点
- **Flow-Noise**：引入可学习噪声网络，将去噪过程建模为离散时间 MDP，实现精确的对数似然计算，使 Flow-based VLA 能在标准 RL 框架下优化
- **Flow-SDE**：将确定性 ODE 转换为等价 SDE，构建双层 MDP 耦合去噪过程与环境交互，并通过混合 ODE-SDE 采样加速训练
- **Critic 架构适配**：针对 π0 和 π0.5 的不同输入结构，设计了不同的 critic 放置策略（VLM 后 vs 动作专家后）
- **数据高效性**：仅需少量专家演示进行 few-shot SFT，后续通过 RL 即可达到甚至超越全数据集 SFT 基线的性能
- **Sim-to-Real 转移**：利用 3D Gaussian Splatting 构建高保真仿真器，实现 zero-shot  sim-to-real 部署

## 实验结果

### Benchmarks
在四个广泛采用的机器人操作基准上评估：LIBERO、ManiSkill、MetaWorld 和 CALVIN。

### In-Distribution (ID) 性能

| Model | LIBERO | ManiSkill | MetaWorld | CALVIN | Avg. | Δ Avg. |
|-------|--------|-----------|-----------|--------|------|--------|
| π0 SFT | 57.6 | 38.4 | 50.8 | 57.5 | 51.1 | — |
| π0 Flow-SDE | 96.1 | 78.8 | 78.1 | 61.7 | 78.7 | +27.6 |
| π0 Flow-Noise | 97.6 | 77.8 | 85.8 | 59.9 | 80.3 | +29.2 |
| π0.5 SFT | 77.1 | 40.1 | 43.8 | 61.3 | 55.6 | — |
| π0.5 Flow-SDE | 97.9 | 90.9 | 70.7 | 87.0 | 86.6 | +31.0 |
| π0.5 Flow-Noise | 98.3 | 89.7 | 66.1 | 84.5 | 84.7 | +29.1 |

- π0 模型平均提升最高达 **+29.2%**，π0.5 模型最高达 **+31.0%**
- 在 LIBERO 上，π0.5 仅用 few-shot SFT + RL 达到 **98.3%** 成功率，超越全数据集 SFT 基线 (96.9%)
- 在 ManiSkill 的 4,352 种 pick-and-place 任务组合上，π0.5 Flow-SDE 达到 **90.9%** 成功率
- 在 CALVIN 长程序列任务上，π0.5 Flow-SDE 将平均完成子任务数从 3.838 提升至 **4.717**，Len-5 成功率从 61.3% 提升至 **87.0%**

### Out-of-Distribution (OOD) 泛化
- **ManiSkill OOD**：在视觉、语义和执行三个 OOD 场景下，RL 训练带来的相对提升与 ID 场景相当（π0.5 Flow-SDE：ID +126.7%，OOD +102.3%），表明 RL 学习到了泛化的动作表示而非过拟合
- **CALVIN ABC→D**：在训练环境 ABC 上 RL 微调后，zero-shot 评估到 Scene D 的成功率从 61.3% 提升至 **79.1%**
- **MetaWorld ML45**：在跨类别任务泛化上表现不稳定，但模型保留了 SFT 阶段学习的 OOD 技能，避免了灾难性遗忘

### 关键结论
- RL 主要提升动作级别的精细化能力，对跨任务的高层泛化能力增强有限
- 冻结 VLM  backbone 限制了视觉泛化能力，未来可考虑使用 LoRA 微调 VLM
- 较低的噪声水平会导致梯度幅度增大，需要更小的学习率保持训练稳定

### Ablation 研究亮点
- **Critic 设计**：对于 π0，VLM 后的 critic ($V_{\mathrm{vlm}}$) 表现略优于动作专家后的 critic，尽管未接收本体感知状态输入
- **MDP 形式化**：单层 MDP (Flow-Noise) 收敛最快，但混合双层 MDP (Flow-SDE) 实现 **2× 加速**
- **噪声策略**：固定噪声与可学习噪声表现相当，但可学习噪声提供更大灵活性
- **去噪步数**：$K=1$ 时训练成功率骤降，表明 ODE-to-SDE 离散化误差显著；增大 $K$ 提升 rollout 性能但增加计算开销
- **Action Chunk**：较大的 chunk size 带来边际性能增益，但减少策略-环境交互频率，降低 RL 优化上限

### Sim-to-Real 验证
在 Franka Panda 机械臂上，使用 3D Gaussian Splatting 构建高保真仿真器，实现 zero-shot sim-to-real 转移。SFT 基线无法完成任务，而 RL 微调策略达到 **40%** 成功率。

![[99_Attachments/papers/images/pirl/5b6aa004f202734af70fa8308988db9b5c276391cbd2e52350c89773f15de366.jpg]]

### GR00T N1.5 扩展实验
将方法扩展到 GR00T N1.5 模型上，在 LIBERO 上取得 **89.9%** 平均成功率，相比 SFT 基线 (52.5%) 提升 **+37.4%**，验证了方法的广泛适用性。

## 个人思考与启发
1. **Flow Matching + RL 的范式意义**：本文成功打通了 Flow-based VLA 与在线 RL 之间的壁垒，为 π0 系列模型的后续优化提供了重要基础。Flow-Noise 和 Flow-SDE 两条路径各有优劣——前者理论更简洁，后者计算更高效。

2. **数据效率的启示**：Few-shot SFT + RL 能够超越全数据集 SFT，这对机器人学习领域意义重大。在实际部署中，收集大量专家数据成本极高，而 πRL 证明了通过环境交互进行策略自我改进的可行性。

3. **OOD 泛化的边界**：实验表明 RL 主要增强动作级别的鲁棒性（视觉变化、执行扰动），但对跨任务语义泛化帮助有限。这提示我们，VLA 的高层任务理解能力可能更多依赖于预训练和 SFT 阶段，RL 更适合作为动作精细化的"后处理"。

4. **可改进方向**：
   - 探索更精细的混合 ODE-SDE 采样策略，而非简单的单步随机选择
   - 尝试在 RL 阶段使用 LoRA 微调 VLM，以增强视觉泛化能力
   - 结合 Flow-CPS 等系数保持采样方法，减少 ODE-to-SDE 转换的精度损失
   - 开发更样本高效的 RL 算法，以实现真实世界中的在线训练

5. **与具身智能研究的关联**：本文的 sim-to-real 方案（3D Gaussian Splatting + RL 微调）为具身智能的实际部署提供了可行路径，值得在相关研究中借鉴。

## 相关论文

- π0: A Vision-Language-Action Flow Model for General Robot Control
- π0.5: A Vision-Language-Action Model with Open-World Generalization
- Flow-GRPO: Training Flow Matching Models via Online RL
- ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning
- RL4VLA: What Can RL Bring to VLA Generalization? An Empirical Study
- RLinf-VLA: A Unified and Efficient Framework for VLA+RL Training
- Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
- Flow Matching for Generative Modeling
- Score-Based Generative Modeling through Stochastic Differential Equations
- GR00T N1: An Open Foundation Model for Generalist Humanoid Robots


## 原文

[[05_Papers/articles/pi-0-6|pi-0-6]]
