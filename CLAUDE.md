# CLAUDE.md

本文件指导 Claude Code 在 `/home/kemove/INNOV/library/` 个人知识库中的工作方式。

## 定位

`library/` 是个人长期知识资产库，不是项目代码库。内容由 Wiki Agent（Claude Code）与本人共同维护，沉淀：

- 论文笔记
- 技术概念整理
- 项目经验复盘
- 决策记录（ADR）
- 实验日志
- 待解决问题

## 核心原则

1. **目录只做粗分类，知识靠链接组织**
   - 不追求一次性完美分类。
   - 优先用 `[[02_AI/Obsidian-Bidirectional-Links|双向链接]]` 和 `#标签` 建立知识网络。

2. **新内容先入 Inbox，再整理**
   - 任何新笔记先放入 `00_Inbox/`。
   - 定期 review，再迁移到对应分类或合并到已有笔记。

3. **概念笔记遵循知识链**
   ```
   Concept → Theory → Paper → Engineering → Experiment → Project
   ```

4. **笔记格式**
   - 使用 YAML frontmatter：`title`, `description`, `tags`, `created`。
   - 正文简洁，1-2 行说清核心。
   - 善用标题、列表、链接，避免大段无结构文本。

## 文件命名

- 英文单词，空格用 `-` 或空格均可（Obsidian 兼容）。
- 例如：`VLA`, `stream-buffer`, `ADR-001-rtc-driver-unification`。

## 目录结构（粗分类）

- [[01_Fundamentals/index|01_Fundamentals]] — 数学、ML、机器人学基础
- [[02_AI/index|02_AI]] — 通用人工智能：LLM、Agent、Prompt Engineering、AI Infra（含 [[02_AI/skills/MinerU-PDF-to-Markdown|MinerU]] 等工具）
- [[03_Robotics/index|03_Robotics]] — 机器人底层技术：感知、规划、控制、硬件、ROS2、工程
- [[04_Embodied-AI/index|04_Embodied-AI]] — 具身智能：VLA、World Model、机器人 RL、具身大脑、Sim2Real
- [[05_Papers/index|05_Papers]] — 论文精读与批注
- [[06_Projects/index|06_Projects]] — 项目经验沉淀
  - [[06_Projects/own/index|own]] — 自己搭建的项目
  - [[06_Projects/external/index|external]] — 外部/开源项目
- [[07_Decisions/index|07_Decisions]] — 决策记录
- [[08_Experiments/index|08_Experiments]] — 实验记录
- [[09_Questions/index|09_Questions]] — 待解决问题

以下是完善后的引导文档 Agent 部分：

---

## Agent 路由指南

### 默认 Agent

涉及以下任务时，应优先使用 `knowledge-manager` Agent：

- 知识整理与笔记创建
- 论文归档后的知识完善
- MOC 构建与技术概念整理
- 知识库结构优化
- Obsidian 双向链接维护
- Inbox 内容处理与归档

`knowledge-manager` 是 library 的**默认维护 Agent**，负责日常知识库运营。

---

### 专项 Agent

#### `paper-researcher`

**适用场景**：

- 新论文归档与深度阅读
- 论文摘要与技术分析
- 论文方法拆解与工程价值评估
- 将论文内容转化为结构化笔记
- 文献综述准备
- 判断某一方法是否可工程落地

**不适用场景**：

- 日常笔记整理（交 `knowledge-manager`）
- 知识体系重构（交 `knowledge-architect`）
- 论文 PDF 格式转换（由 MinerU 处理）

**触发关键词**：论文、paper、文献、arXiv、方法分析、工程可行性、模型架构解析

---

#### `knowledge-architect`

**适用场景**：

- 知识库整体健康审计
- MOC 设计与重构
- 知识图谱拓扑优化
- 分类体系调整
- 跨领域知识关系发现
- 知识库长期演化路线规划

**不适用场景**：

- 单篇论文处理（交 `paper-researcher`）
- 日常笔记维护（交 `knowledge-manager`）
- 具体内容修改（交 `knowledge-manager`）

**触发关键词**：知识库审计、重构、MOC 设计、体系优化、分类调整、结构梳理、知识拓扑

---

### 选择决策树

```text
用户请求
    ↓
判断任务类型
    ↓
┌─────────────────────────────────────────────┐
│ 是否涉及论文深度分析/技术提取？              │
│    是 → paper-researcher                    │
│    否 ↓                                     │
│ 是否涉及知识库结构/体系顶层设计？            │
│    是 → knowledge-architect                 │
│    否 ↓                                     │
│ 默认 → knowledge-manager                    │
└─────────────────────────────────────────────┘
```

---

### Agent 职责边界速查

| Agent | 职责 | 主要产出 |
|-------|------|----------|
| `knowledge-manager` | 日常知识维护、笔记创建、链接建设 | 笔记、链接、MOC 条目 |
| `paper-researcher` | 论文深度处理、技术分析、工程评估 | 结构化论文笔记 |
| `knowledge-architect` | 体系审计、MOC 设计、拓扑优化 | 审计报告、MOC、演化方案 |

---

### Agent 协作链路

```text
新论文导入
    ↓
paper-researcher 完成深度笔记
    ↓
knowledge-manager 完善链接与归档
    ↓
（积累至阈值）
    ↓
knowledge-architect 触发 MOC 重构
```


## 禁止事项

- 不要把项目代码放入 `library/`。
- 不要把临时下载文件直接放根目录，统一进 `00_Inbox/` 或 `99_Attachments/`。
- 不要创建过深的目录层级（建议最多 3 层）。

## Python 环境

本项目使用 `uv` 管理 Python 3.12 虚拟环境，环境位于 `.venv/`。Claude Code 已通过 `.claude/settings.local.json` 自动注入 `VIRTUAL_ENV` 与 `PATH`，Bash 工具中 `python`、`uv` 等命令会优先使用项目环境。

## 自动化技能

项目已内置两个 Claude Code skill：

- `/archive-papers`：将 `00_Inbox/` 中的论文自动归档到 `05_Papers/`（MinerU 转换、分类推断、slug 生成、笔记生成、索引更新）。技能文件位于 `.claude/skills/archive-papers/`。
- `/mineru-pdf-to-markdown`：将 PDF/图片/Office 文档转换为 Markdown。技能文件位于 `.claude/skills/mineru-pdf-to-markdown.skill`。

每次会话启动时，如果 `00_Inbox/` 有待归档论文，会自动提示运行 `/archive-papers`。配置位于 `.claude/settings.local.json`。

## 相关入口

- [[00_Inbox/index|00_Inbox]]
- [[09_Questions/index|09_Questions]]
- [[07_Decisions/index|07_Decisions]]
- [[Templates/index|Templates]]

