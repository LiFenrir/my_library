# 分类判断：Vision-Language-Action (VLA) 应放到哪个目录

## 提取内容

从 `05_Papers/articles/pi0-7.md` 的 **III. Flow-based Vision-Language-Action Models** 章节提取到：

1. **通用定义**：VLA 从预训练 VLM 出发，输入历史观测（多视角图像 + 本体状态）与上下文提示，输出未来动作块。
2. **训练目标**：最大化动作块在观测与上下文条件下的近似对数似然：
   $$
   \max_{\theta} \mathbb{E}_{\mathcal{D}} \left[ \log \pi_{\theta}\left(\mathbf{a}_{t:t+H} \mid \mathbf{o}_{t-T:t}, \mathcal{C}_t\right) \right]
   $$
3. **关键组件**：VLM backbone、Action expert、Flow matching/diffusion 目标、Knowledge insulation、上下文 prompt（语言指令、子目标图像、episode 元数据等）。

## 候选目录分析

| 候选目录 | 目录定位 | 是否合适 | 理由 |
|---------|---------|---------|------|
| `02_AI/LLM` | 通用人工智能：不绑定具体硬件 embodiment 的方法 | 不合适 | VLA 的动作输出直接控制物理机器人，必须依赖具体 embodiment，不属于通用 AI 范畴。`02_AI/index.md` 明确将 VLA 指向 `04_Embodied-AI`。 |
| `01_Fundamentals/Robotics-Foundation` | 机器人学数学与物理基础（运动学、动力学等） | 不合适 | VLA 是深度学习模型与策略方法，不是机器人学基础理论。 |
| `03_Robotics/Control` 或 `Planning` | 机器人底层控制与规划 | 不合适 | VLA 属于高层数据驱动策略/具身模型，而非传统控制或规划算法。`03_Robotics/index.md` 也明确将 VLA 指向 `04_Embodied-AI`。 |
| `04_Embodied-AI/VLA` | 具身智能：VLA、World Model、机器人 RL 等 | **合适** | `04_Embodied-AI/index.md` 明确列出“VLA — Vision-Language-Action 模型、机器人策略”作为子领域；VLA 同时融合视觉、语言、动作，并直接作用于物理 embodiment。 |

## 结论

**Vision-Language-Action (VLA) 应放入 `04_Embodied-AI/VLA/`。**

虽然 VLA 涉及通用多模态 AI（VLM、语言理解），但其核心特征是：
- 输出为机器人动作；
- 训练与推理都围绕物理 embodiment 展开；
- 与机器人控制、跨本体迁移、Sim2Real 等具身智能问题强耦合。

因此按知识库当前的目录边界，VLA 属于具身智能而非通用 AI 或机器人底层技术。

## 产出文件

- `vision-language-action.md`：VLA 通用定义与训练目标笔记
- `summary.md`：本分类判断说明
