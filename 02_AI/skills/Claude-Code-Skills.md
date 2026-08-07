---
title: "Claude Code Skills"
description: "本知识库中使用的 Claude Code skill 索引"
tags: [reference, claude-code, skill, ai-infra]
created: 2026-07-31
---

# Claude Code Skills

本笔记汇总 `library/` 知识库中使用的 Claude Code skill，方便查找与维护。

## 项目 Skill（`.claude/skills/`）

- [[02_AI/skills/arxiv-pdf-downloader|arXiv PDF Downloader]] — 按 ID/标题下载论文 PDF 到 `00_Inbox/`
- [[02_AI/skills/MinerU-PDF-to-Markdown|MinerU PDF-to-Markdown]] — 将 PDF/图片/Office 文档转换为 Markdown
- [[02_AI/skills/archive-papers|Archive Papers]] — 自动归档 Inbox 中的论文到 `05_Papers/`
- [[02_AI/skills/extract-paper-knowledge|Extract Paper Knowledge]] — 论文通用知识沉淀到 01-04 知识目录

## 用户级 Skill（`~/.claude/skills/`）

- `codegraph-init` / `codegraph-status` / `codegraph-update` — codegraph 代码索引的初始化与维护
- `arxiv-downloader`、`archive-papers`、`mineru-pdf-to-markdown` — 上述项目 skill 的用户级副本

## 论文处理流水线

```
arxiv-pdf-downloader → mineru-pdf-to-markdown → archive-papers → extract-paper-knowledge
   (下载 PDF)            (PDF → Markdown)          (归档+笔记)        (沉淀通用知识)
```

## 相关

- [[02_AI/skills/claude-code-plugins-mcp|Claude Code 插件与 MCP 工具推荐]] — skill 依赖的 MCP 与插件生态
- [[00_Inbox/index|00_Inbox]] — 待处理入口
- [[05_Papers/index|05_Papers]] — 论文归档目录
