---
title: Archive Papers Skill
description: Claude Code skill，自动将 00_Inbox 中的论文归档到 05_Papers。
tags: [claude-code, skill, archive-papers, pdf, mineru, obsidian, workflow]
created: 2026-07-22
---

# Archive Papers Skill

Claude Code skill，将 `library/00_Inbox/` 中的论文自动归档到 `05_Papers/` 规范目录，并生成结构化笔记、更新索引。

## 触发方式

在 library 项目内对 Claude 说：

- "归档论文"
- "/archive-papers"
- "把 Inbox 里的论文整理一下"

## 文件位置

- 项目内 Skill 说明：`.claude/skills/archive-papers/SKILL.md`
- 辅助脚本：`.claude/skills/archive-papers/scripts/archive_papers.py`
- 使用说明：`.claude/skills/archive-papers/README.md`
- 归档示例：`.claude/skills/archive-papers/examples/phail.md`

## 归档目标结构

```
library/
├── 00_Inbox/
│   └── arxiv-XXXX.XXXXX.pdf          # 源，归档后删除
├── 05_Papers/
│   ├── articles/
│   │   └── <slug>.md                    # MinerU 原文，标题优化过
│   ├── notes/
│   │   └── <slug>.md                    # 人工整理笔记
│   └── index.md                         # 分类入口 + 统计数
└── 99_Attachments/papers/
    ├── pdfs/<slug>.pdf
    └── images/<slug>/*.jpg
```

## 执行流程

1. **扫描 Inbox**：识别 `arxiv-*.pdf` 或已转换的 `arxiv-*/full.md` 目录。
2. **MinerU 转换**：对仅有 PDF 的项调用 `/mineru-pdf-to-markdown` skill。
3. **元信息推断**：读取原文，提取标题、作者、机构、链接、摘要，推断分类和 slug。
4. **生成笔记**：按模板生成 `05_Papers/notes/<slug>.md`。
5. **迁移文件**：移动原文、PDF、图片到规范位置。
6. **更新索引**：在 `05_Papers/index.md` 对应分类区添加链接并更新统计数。

## 支持分类

| 分类 | 说明 |
|---|---|
| `vla` | Vision-Language-Action 模型、机器人策略 |
| `world-model` | 世界模型、视频预测、环境动力学 |
| `world-action-model` | 世界动作模型 |
| `embodied-ai` | 具身智能、机器人学习 |
| `rl` | 强化学习算法 |

## 可选参数

- `/archive-papers --dry-run`：只预览，不移动文件。
- `/archive-papers --auto`：自动推断分类/slug，不逐篇询问。
- `/archive-papers --category vla`：强制指定分类。
- `/archive-papers --slug my-slug`：强制指定 slug（仅单篇时有效）。

## 自动化提醒

项目已配置 `SessionStart` hook。每次进入 library 项目时，如果 `00_Inbox/` 有待归档论文，会自动提示：

```
📥 检测到 00_Inbox 有 N 项待归档论文，可运行 /archive-papers 自动整理。
```

配置位于 `.claude/settings.local.json`。

## 与项目目录的关系

- [[00_Inbox/index|00_Inbox]] — 论文临时入口
- [[05_Papers/index|05_Papers]] — 论文归档专区
- [[02_AI/skills/MinerU-PDF-to-Markdown|MinerU-PDF-to-Markdown]] — 本 skill 依赖的 PDF 转换工具

## 已知限制

- 分类推断基于标题和摘要，跨领域论文可能需手动调整。
- slug 冲突时自动追加后缀（如 `-2`）。
- MinerU 转换需要有效 API token。
- 完整流程尚未在真实论文上端到端验证。
