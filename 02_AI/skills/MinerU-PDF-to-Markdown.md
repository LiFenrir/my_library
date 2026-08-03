---
title: MinerU PDF-to-Markdown Skill
description: Claude Code skill，调用 MinerU 精准 API 将 PDF/图片/Office 文档转为 Markdown。
tags: [claude-code, skill, mineru, pdf, markdown, obsidian]
created: 2026-07-22
---

# MinerU PDF-to-Markdown Skill

Claude Code skill，调用 MinerU 精准解析 API 将 PDF、图片、Office 文档转换为 Markdown。

## 触发方式

对 Claude 说：

- "把这份 PDF 转成 Markdown"
- "用 MinerU 解析这个论文"
- "批量把这几个 PDF 转成 Markdown，用于 RAG"

## 文件位置

- 项目内 Skill 包：`.claude/skills/mineru-pdf-to-markdown.skill`
- 全局 Skill 包（旧位置）：`~/.claude/skills/mineru-pdf-to-markdown.skill`
- Token：`~/.mineru/config`

## 支持的输入

- PDF、图片（png/jpg/jpeg/jp2/webp/gif/bmp）
- Word（doc/docx）、PPT（ppt/pptx）、Excel（xls/xlsx）
- 单文件 URL 或本地文件
- 批量 URL 或本地文件

## 输出结构

对 `paper.pdf` 默认生成目录 `paper/`：

```
paper/
├── full.md          # Markdown 文本
├── full.html        # HTML 完整渲染版
├── full.tex         # LaTeX 版
├── images/          # 论文图片
├── layout.json      # 版面分析
└── content_list.json
```

## 关键特性

1. **图片保留**：解压完整 ZIP，`full.md` 中的 `![](images/...)` 引用有效。
2. **表格增强**：用 `full.html` 中的 `<table>` 生成 Markdown 表格，替换 `full.md` 中的纯文本块。
3. **公式保留**：Markdown 中以 LaTeX 形式保留；复杂公式建议直接查看 `full.html`。

## Obsidian 使用建议

Obsidian 表格单元格不支持块级 `$$...$$` 公式或复杂 LaTeX（如 `\frac`、多行结构）。

- 用 `full.md` 做文本搜索、编辑、简单内容
- 用 `full.html` 查看完整表格和公式渲染

## 命令行脚本

Skill 内部调用 `scripts/mineru_convert.py`：

```bash
python scripts/mineru_convert.py <input> [output.md or output_dir] \
  [--model vlm|pipeline|MinerU-HTML] \
  [--ocr] [--no-table] [--no-formula] \
  [--language ch] \
  [--page-ranges "1-5,8"] \
  [--extra-formats html,latex]
```

常用示例：

```bash
# 本地 PDF，输出到同名目录，同时导出 HTML
python scripts/mineru_convert.py paper.pdf --model vlm --extra-formats html,latex

# 指定输出 Markdown 路径
python scripts/mineru_convert.py paper.pdf output/paper.md --extra-formats html
```

## 限制

- 文件大小 ≤ 200MB，页数 ≤ 200 页
- 需要 MinerU API token
- URL 端点偶尔 pending 超时，本地文件上传更稳定

## 相关

- [[00_Inbox/index|00_Inbox]]
- [[05_Papers/index|05_Papers]]
- [[02_AI/skills/Claude-Code-Skills|Claude Code Skills]]
