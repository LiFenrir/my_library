---
title: Extract Paper Knowledge Skill
description: Claude Code skill，把论文的通用知识（背景/相关工作/理论）沉淀到 01-04 知识目录。
tags: [claude-code, skill, knowledge-extraction, papers, workflow]
kind: skill
created: 2026-08-07
---

# 论文通用知识提取 Skill

本 skill 负责把 `05_Papers/articles/` 中论文的「研究背景 / 相关工作 / 理论基础 / 方法原理」等通用段落，沉淀到 `01_Fundamentals/`、`02_AI/`、`03_Robotics/`、`04_Embodied-AI/` 四个长期知识目录。

## 触发条件

用户表达以下意图时立即触发：

- "从论文 X 提取通用知识"
- "把论文的研究背景/相关工作整理到 01/02/03/04"
- "批量补充 01-04 的基础概念"
- "根据论文理论部分生成概念笔记"
- "把 05_Papers 沉淀到通用知识库"

## 输入

- 单篇论文：`05_Papers/articles/<paper-slug>.md`
- 批量：用户指定多篇论文，或要求处理整个 `05_Papers/articles/`
- 用户可能指定目标领域（01/02/03/04），也可能不指定

## 输出

- 在 `01_Fundamentals/`、`02_AI/`、`03_Robotics/` 或 `04_Embodied-AI/` 下创建或追加的 Markdown 笔记
- 每篇新笔记遵循项目统一的 YAML frontmatter：title、description、tags、created
- 生成处理摘要，列出：读取论文、识别章节、提取概念、目标路径、操作（创建/追加/跳过）、原因

## 核心流程

### 1. 读取并切片论文

读取目标论文 Markdown，定位以下通用知识章节（标题匹配不区分大小写，支持 #/##/###）：

- Introduction / 引言 / 简介 / 研究背景
- Related Work / 相关工作 / 文献综述
- Background / 背景
- Preliminaries / 预备知识
- Methodology / 方法 / 方法概述（仅提取通用方法原理，不保留论文专属实验细节）
- Theory / 理论基础 / Theoretical Background
- Discussion / 讨论（仅提取通用观点与局限性）

忽略以下章节：

- Abstract（摘要已在论文笔记中）
- Experiments / 实验
- Results / 结果
- Evaluation / 评估
- Ablation Studies / 消融实验
- Conclusion / 结论
- Acknowledgement / 致谢
- References / 参考文献
- Appendix 中的具体实现细节

### 2. 提取通用知识单元

从上述章节中提取以下粒度：

- **核心概念与术语**：给出定义、符号表示、与其他概念的关系
- **方法原理**：模型/算法/框架的通用思想、关键步骤、损失函数、优化目标
- **公式**：保留对理解概念必要的公式，说明每个符号含义
- **优缺点 / 适用条件 / 局限性**：区分这是论文提出的方法还是领域通用认知
- **相关概念链接**：使用 Obsidian 双向链接 `[[note-slug|显示名]]` 指向已有笔记

注意：不要把论文的「具体实现细节」「实验配置」「数据集」「作者自夸」当作通用知识。

### 3. 判断所属领域

根据概念本身的通用归属，而非论文的应用场景：

- `01_Fundamentals/` — 数学、统计、机器学习基础理论、机器人学数学/物理基础
- `02_AI/` — 不绑定具体 embodiment 的 AI 方法：LLM、VLM、Agent、Prompt Engineering、AI Infra、通用训练/推理技术、通用视觉/多模态模型
- `03_Robotics/` — 机器人底层技术：感知、规划、控制、硬件、ROS2、机器人工程
- `04_Embodied-AI/` — 绑定物理/仿真身体的 AI：VLA、World Model、Robot RL、Sim2Real、具身大脑

**边界规则**：

- 若一个概念同时属于 `02_AI` 和 `04_Embodied-AI`，优先归入 `02_AI`（通用 AI）。例如：Vision Transformer、LLM、Diffusion Model、Flow Matching、MoE 等基础模型方法放在 `02_AI`；而 VLA 架构、机器人策略学习、Sim2Real 放在 `04_Embodied-AI`。
- 若用户明确指定目标领域，按用户指定执行。
- 若无法判断，先归入 `00_Inbox/` 并标注待 review，不直接写入 01-04。

### 4. 检查并匹配现有笔记

在目标领域（含子目录）搜索主题相似的现有笔记：

- 读取候选笔记的 frontmatter 与正文前 30 行
- 判断主题是否相同或高度相关

**决策分支**：

- **已有相同主题笔记**：
  - 分析待写入内容与现有笔记的差异
  - 若有新信息、新角度、新补充：追加到现有笔记末尾，或合并到合适章节
  - 若完全相同或现有笔记已覆盖：跳过，记录原因
  - 追加时保持原笔记风格，添加 `来自 [[05_Papers/notes/<paper-note>|论文标题]]` 的引用
- **没有相同主题笔记**：
  - 创建新笔记，文件名为英文短横线连接（如 `vision-transformer.md`、`flow-matching.md`）
  - 放在目标领域最合适的子目录下；若子目录不确定，直接放在目标领域根目录
  - frontmatter：title、description、tags、created
  - 正文：概念定义、原理、公式、优缺点、相关链接、来源引用

### 5. 信息补充（可选但推荐）

当论文某段内容不完整、术语较新、或需要补充通用定义时：

- 使用 WebSearch 搜索该术语的通用解释
- 使用 WebFetch 抓取权威来源（如官方博客、arXiv、教程页面）
- 把补充内容整合到笔记中，并标注来源

不要过度补充：优先使用论文自身内容，只在必要时搜索。

## 笔记格式

### 新笔记 frontmatter

```yaml
---
title: "Concept Name"
description: "一句话概括这个概念/方法"
tags: [concept, ai, llm]
created: 2026-07-28
---
```

### 正文结构建议

```markdown
# Concept Name

核心定义：1-2 句话说明是什么。

## 原理

方法原理与关键步骤。

## 公式

必要公式及符号说明。

## 优缺点

- 优点：...
- 缺点 / 局限：...

## 与其他概念的关系

- [[related-concept|相关概念]] — 关系说明

## 来源

- [[05_Papers/notes/<paper-note>|论文标题]]
```

## 追加到现有笔记的格式

在笔记末尾或合适章节追加：

```markdown
## 补充：来自 [[05_Papers/notes/<paper-note>|论文标题]]

- 新角度 / 新细节：...
- 论文中的表述：...
```

## 处理摘要

每轮处理结束后，向用户返回处理摘要：

```markdown
# 论文通用知识提取摘要

## 处理论文

- [[05_Papers/articles/<paper>|论文标题]]

## 识别章节

- Introduction / Related Work / ...

## 提取概念

1. **Concept A** → `02_AI/LLM/concept-a.md`（创建）
2. **Concept B** → `02_AI/Agent/concept-b.md`（追加，补充了 X）
3. **Concept C** → `04_Embodied-AI/VLA/concept-c.md`（跳过，已有笔记覆盖）

## 未处理

- 实验细节（按规则忽略）
- 某模糊概念（已放入 00_Inbox/ 待 review）
```

## 禁止事项

- 不要把论文专属实现细节、实验结果、数据集写入 01-04。
- 不要创建过深的目录层级（最多 3 层）。
- 不要把临时文件直接放根目录。
- 不要覆盖或删除现有笔记内容，只能追加。
- 不要在函数内部使用 inline import，所有依赖放在文件顶部。

## 批量处理模式

当用户要求"批量补充"或"处理所有论文"时：

1. 列出 `05_Papers/articles/` 下所有 `.md` 文件
2. 优先处理用户未明确指定的论文；如果论文数量过多，先处理最近归档的或用户指定的子集
3. 对每篇论文执行上述流程
4. 汇总所有处理摘要，避免重复提取同一概念
5. 若发现多篇论文指向同一个通用概念，合并到同一笔记，而不是创建多个重复笔记
