# 论文通用知识提取摘要

## 处理论文

- [[05_Papers/articles/pi0-7|π0.7: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities]]

## 识别章节

读取并提取通用知识的章节：

- I. Introduction（引言）
- II. Related Work（相关工作）
- III. Flow-based Vision-Language-Action Models（基于流的 VLA 模型）
- IV. π0.7 Overview（模型概述）
- V. Diversifying the Prompt（多样化提示）
- VI. The π0.7 Model and Training Recipe（模型与训练方法）
- VII. Prompting π0.7 at Runtime（运行时提示）
- X. Discussion（讨论）

忽略的章节：

- Abstract（已在论文笔记中）
- VIII. Robot System Details（具体硬件与实现细节）
- IX. Experimental Evaluation（实验、结果、消融）
- References / Appendices（实现细节与任务评分细则）

## 提取概念

| # | 概念 | 目标路径 | 操作 | 原因 |
|---|------|----------|------|------|
| 1 | Flow Matching Action Expert | `02_AI/LLM/flow-matching-action-expert.md` | 创建 | 通用生成模型方法，不绑定具体 embodiment；按边界规则优先归入 02_AI。 |
| 2 | VLA Architecture | `04_Embodied-AI/VLA/vla-architecture.md` | 创建 | VLA 架构属于具身智能核心概念。 |
| 3 | Prompt Conditioning for VLA | `04_Embodied-AI/VLA/prompt-conditioning-for-vla.md` | 创建 | 多模态提示条件是 VLA/具身智能特有的方法，π0.7 的核心贡献。 |
| 4 | Knowledge Insulation | `04_Embodied-AI/VLA/knowledge-insulation.md` | 创建 | VLA 训练 recipe，与 VLA 架构强绑定。 |
| 5 | Action Chunking and RTC | `04_Embodied-AI/VLA/action-chunking-and-rtc.md` | 创建 | VLA 推理工程方法，虽然 RTC 也可泛化到控制，但当前论文上下文是 VLA。 |

## 边界判断与未处理项

- **Flow Matching 本身 vs Flow Matching Action Expert**：论文中 flow matching 是作为 action expert 的训练目标出现的，因此提炼为“Flow Matching Action Expert”这一应用形态，而非纯数学 flow matching。若 01_Fundamentals/ML 未来需要更基础的 flow matching 笔记，可作为上游补充。
- **Subgoal Image Generation / World Model**：论文中用于生成子目标图像的 lightweight world model 属于 world model 范畴，可考虑归入 `04_Embodied-AI/World-Model/`；但 π0.7 里它主要服务于 VLA 提示，为避免过度拆分，当前将其并入 `prompt-conditioning-for-vla.md` 的“子目标图像”一节。
- **Cross-embodiment Generalization / Compositional Task Generalization**：属于 VLA/具身智能的能力表现，已在 `vla-architecture.md` 和 `prompt-conditioning-for-vla.md` 中作为关系/效果提及，未单独成篇，避免与 04_Embodied-AI 未来更宏观的笔记重复。
- **Episode Metadata / Control Mode**：作为 Prompt Conditioning 的组成部分，合并到同一篇笔记，避免碎片化。
- **未创建 03_Robotics 笔记**：论文未深入涉及底层感知、规划、控制理论或 ROS2 等 03_Robotics 专属内容。

## 现有笔记检查

已检查 01-04 目录下现有 `.md` 文件：

- `01_Fundamentals/index.md`、`01_Fundamentals/Robotics-Foundation/index.md`
- `02_AI/index.md`、`02_AI/skills/*`
- `03_Robotics/index.md`、`03_Robotics/Robot-SDK/index.md`
- `04_Embodied-AI/index.md`

未发现与上述 5 个概念主题相同或高度重复的现有笔记，因此全部新建。

## 输出文件列表

```
extract-paper-knowledge-workspace/iteration-1/eval-1/with_skill/outputs/
├── 02_AI/
│   └── LLM/
│       └── flow-matching-action-expert.md
├── 04_Embodied-AI/
│   └── VLA/
│       ├── vla-architecture.md
│       ├── prompt-conditioning-for-vla.md
│       ├── knowledge-insulation.md
│       └── action-chunking-and-rtc.md
└── summary.md
```
