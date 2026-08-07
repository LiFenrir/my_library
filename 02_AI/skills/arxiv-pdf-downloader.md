---
title: arXiv PDF Downloader Skill
description: Claude Code skill，按 arXiv ID 或标题搜索并下载论文 PDF 到 00_Inbox。
tags: [claude-code, skill, arxiv, pdf, workflow]
kind: skill
created: 2026-08-07
---

# arXiv PDF 下载器

把 arXiv 论文按 ID 或标题检索，并下载原始 PDF 到 `00_Inbox/`。

## 触发条件

- 用户提到“下载 arxiv 论文”、“arxiv PDF”、“下论文”等。
- 用户给出 arXiv ID（如 `2608.02580v1`）或论文标题/关键词。

## 执行流程

### 1. 解析输入

判断用户给的是 arXiv ID 还是标题：

- arXiv ID 模式：数字.数字（可带 vN 后缀），例如 `2608.02580v1`、`2608.02580`。
- 否则视为标题或关键词。

### 2. 标题 → 搜索

若输入为标题，调用：

```
mcp__arxiv__search_papers
  query: <标题关键词>
  categories: [cs.RO, cs.LG, cs.AI, cs.CV, cs.CL]
  max_results: 10
  sort_by: relevance
```

取第一条结果的 `id` 作为候选，并向用户确认是否匹配。

### 3. 确认论文存在

调用：

```
mcp__arxiv__get_abstract
  paper_id: <id>
```

- 若返回错误/不存在，告知用户未找到，并停止。
- 若成功，提取标题，用于生成文件名 slug。

### 4. 下载 PDF

运行辅助脚本：

```bash
python3 .claude/skills/arxiv-pdf-downloader/scripts/download_arxiv_pdf.py \
  <arxiv_id> --title "<论文标题>" --out-dir 00_Inbox
```

输出路径格式：

```
00_Inbox/<slug>-<arxiv_id>.pdf
```

例如：

```
00_Inbox/Ego2Robot-Scalable-Robot-Data-Synthesis-2608.02580v1.pdf
```

### 5. 报告结果

告诉用户：

- 是否下载成功
- 保存路径
- 文件大小

## 错误处理

- **标题无结果**：告知用户未找到匹配论文，建议换关键词或提供 arXiv ID。
- **get_abstract 失败**：提示论文可能尚未发布或 ID 错误。
- **下载失败**：报告 HTTP 状态码/异常信息，保留 Inbox 中已有文件不变。
- **文件已存在**：提示用户是否覆盖；默认不覆盖。

## 输出示例

```
已下载：Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data
保存至：00_Inbox/Ego2Robot-Scalable-Robot-Data-Synthesis-2608.02580v1.pdf
大小：12.3 MB
```
