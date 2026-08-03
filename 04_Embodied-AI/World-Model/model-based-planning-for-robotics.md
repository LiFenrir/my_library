---
title: "Model-Based Planning for Robotics"
description: "机器人利用习得的世界模型与价值函数进行动作搜索与规划的范式，包括 best-of-N 采样、rollout 精炼与价值函数集成"
tags: [concept, embodied-ai, model-based-rl, planning, world-model]
created: 2026-07-30
---

# Model-Based Planning for Robotics

**核心定义**：Model-Based Planning for Robotics 是指机器人利用学习得到的世界模型（world model）预测未来状态，并结合价值函数（value function）评估这些未来状态，从而在测试时搜索更高成功概率动作轨迹的范式。

## 核心动机

纯模仿学习只能复现训练分布内的成功轨迹。当任务涉及：

- 高动作多模态（如多目标可选）
- 长程时序依赖
- 高精度接触操作

仅依赖直接策略容易失败。通过世界模型想象多个候选动作的未来结果并选择最优者，可以提升成功率。

## 关键组件

1. **策略模型（Policy Model）**：生成候选动作提案
2. **世界模型（World Model）**：$\hat{T}: S \times A \to \Pi(S)$，预测执行动作后的未来状态
3. **价值函数（Value Function）**：$V^\pi(s) = \mathbb{E}_{\tau \sim \pi} \left[ \sum_{k=t}^{H} \gamma^{k-t} R(s_k, a_k) \mid s_t = s \right]$，评估未来状态的期望回报

## Best-of-N 规划流程

1. **采样候选动作**：从策略模型中采样 $N$ 个动作提案
2. **预测未来状态**：用世界模型对每个动作提案预测未来状态
3. **评估未来价值**：用价值函数对每个预测未来状态打分
4. **选择执行**：选择价值最高的动作执行

$$
a^* = \arg\max_{a_i} V(s'_i), \quad s'_i \sim \hat{T}(s, a_i)
$$

## 提升预测可靠性的技术

### Ensemble 与 Majority Mean

为处理多峰或高方差的价值分布，可对预测做集成：

- 对每个动作采样多个未来状态（如 3 次）
- 对每个未来状态采样多个价值（如 5 次）
- 得到 $N \times 3 \times 5$ 个价值预测
- 用 majority mean：判断多数预测为成功或失败，再在多数组内取平均

这比朴素平均对 outlier 更鲁棒。

### 从 Rollout 经验精炼

训练数据如果只包含成功演示，世界模型和价值函数只能看到狭窄的状态-动作分布。通过收集策略 rollout 数据（包含失败），可以：

- 扩展世界模型对失败状态的覆盖
- 让价值函数学会区分成功与失败
- 采用 dual checkpoint 策略：原始策略模型生成提案，精炼后的规划模型负责世界模型与价值预测

典型训练配比：90% 数据用于世界模型和价值函数训练，10% 用于策略训练。

## 价值函数变体

| 形式 | 条件 | 用途 |
|------|------|------|
| **State Value** $V(s')$ | 仅依赖未来状态 | 需要世界模型，模型驱动规划 |
| **State-Action Value** $Q(s, a)$ | 依赖当前状态与动作 | 可直接规划，无需世界模型（model-free planning） |
| **Successor Value** $V(s, a, s')$ | 依赖完整转移 | 训练时提供辅助监督 |

实践中，模型驱动的 $V(s')$ 通常比 model-free 的 $Q(s,a)$ 样本效率更高、规划效果更好。

## 优缺点

- **优点**：可利用 rollout 数据持续改进；规划能找到训练分布外的更优动作；世界模型提供可解释的未来预测
- **缺点/局限**：推理速度显著慢于直接策略（如每动作块需数秒）；需要额外 rollout 数据；单步规划深度有限；模型误差会累积

## 与其他概念的关系

- [[01_Fundamentals/ML/Model-Based-Reinforcement-Learning|Model-Based Reinforcement Learning]] — 模型驱动规划的方法论基础
- [[04_Embodied-AI/World-Model/World-Model|World Model]] — 规划使用的环境内部模型
- [[04_Embodied-AI/World-Model/video-foundation-model-for-robotics|Video Foundation Model for Robotics]] — 可作为统一策略/世界模型/价值函数的基础
- [[04_Embodied-AI/World-Model/latent-frame-injection|Latent Frame Injection]] — 在视频模型中统一实现策略、世界模型、价值函数的方法

## 来源

- [[05_Papers/articles/cosmos-policy|COSMOS POLICY: Fine-Tuning Video Models for Visuomotor Control and Planning]]，第 4.2、4.3、5.3、6 节
