---
name: archive-papers
description: 将 00_Inbox 中的论文自动归档到 05_Papers：MinerU 转换、slug 生成、笔记生成、图片路径重写、索引更新。
compatibility: 依赖项目结构 00_Inbox/、05_Papers/、99_Attachments/papers/；需要 MinerU API token 或已转换的 full.md 目录。
---

# Archive Papers

把 `00_Inbox/` 中的论文迁移到 `05_Papers/` 规范目录，并生成结构化笔记、重写图片路径、更新索引。

## 触发条件

用户输入 `/archive-papers` 时调用。可选参数：

- `--dry-run`：只预览，不移动文件。
- `--auto`：自动推断 slug，不逐篇询问。
- `--slug <slug>`：强制指定 slug（仅单篇时有效）。

## 归档目标结构

```
library/
├── 00_Inbox/
│   └── arxiv-XXXX.XXXXX.pdf          # 源，归档后删除
├── 05_Papers/
│   ├── articles/
│   │   └── <slug>.md                    # MinerU 原文，平铺，图片路径已重写
│   ├── notes/
│   │   └── <slug>.md                    # 人工整理笔记
│   └── index.md                         # 平铺论文列表 + 统计数
└── 99_Attachments/papers/
    ├── pdfs/<slug>.pdf
    └── images/<slug>/*.jpg
```

## 执行流程

### 1. 扫描 Inbox

运行辅助脚本获取候选列表：

```bash
python3 .claude/skills/archive-papers/scripts/archive_papers.py scan
```

候选分两类：
- 仅有 PDF（如 `arxiv-2605.29710.pdf`）
- 已转换目录（如 `arxiv-2605.29710/full.md` + `images/`）

### 2. 转换 PDF（如需要）

若候选只有 PDF，先调用 MinerU 转换为 markdown：

- 使用项目内 skill `/mineru-pdf-to-markdown`（位于 `.claude/skills/mineru-pdf-to-markdown.skill`）。
- 输出到 `00_Inbox/<arxiv-id>/full.md` 与 `00_Inbox/<arxiv-id>/images/`。

### 3. 读取原文并推断元信息

读取 `full.md` 的前 200 行左右，提取：
- 标题
- 作者
- 机构
- arXiv 链接
- 项目/代码链接
- 摘要
- 核心方法、实验设置、主要结果、局限

生成 slug：
- 规则：小写、英文单词用连字符、去掉冠词/介词、长度 ≤ 40 字符。
- 例如标题 "PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology" -> `phail`。

若未加 `--auto`，向用户确认 slug。

### 4. 生成笔记

在 `05_Papers/notes/<slug>.md` 写入结构化笔记，模板如下：

```markdown
---
title: "<论文标题>"
description: "<一句话概括>"
tags: ["<关键词>", ...]
created: <YYYY-MM-DD>
---

# <论文标题>

## 基本信息

- **作者**: ...
- **机构**: ...
- **链接**: [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)
- **发表**: ...
- **原文**: [[05_Papers/articles/<slug>.md|<slug>]]
- **PDF**: [[99_Attachments/papers/pdfs/<slug>.pdf|<slug>.pdf]]

## 研究背景

...

## 核心方法

...

## 实验设置

...

## 主要结果

...

## 个人思考与启发

1. ...
2. ...

## 局限与未来

...

## 相关论文

- [[slug|title]]
```

### 5. 迁移文件并更新索引

运行辅助脚本：

```bash
python3 .claude/skills/archive-papers/scripts/archive_papers.py move \
  --slug <slug> --pdf <源pdf路径> --dir <源目录路径>
```

该脚本会：
- 移动 PDF 到 `99_Attachments/papers/pdfs/<slug>.pdf`
- 移动图片到 `99_Attachments/papers/images/<slug>/`
- 将 `full.md` 写入 `05_Papers/articles/<slug>.md`，并将其中 `images/xxx` 重写为 `../../99_Attachments/papers/images/<slug>/xxx`
- 清理空源目录

然后更新索引：

```bash
python3 .claude/skills/archive-papers/scripts/archive_papers.py update-index \
  --slug <slug>
```

### 6. 清理

删除空的 `00_Inbox/arxiv-XXXX.XXXXX/` 目录。

## 错误处理

- 若 Inbox 为空，直接告知用户。
- 若 slug 冲突，追加短后缀（如 `-2`）并提示用户。
- 若 MinerU 转换失败，保留 PDF 在 Inbox，报告失败项。

## 输出示例

归档完成后报告：

```
已归档 1 篇论文：
- ego2robot -> 05_Papers/notes/ego2robot.md
- 原文 -> 05_Papers/articles/ego2robot.md
- PDF -> 99_Attachments/papers/pdfs/ego2robot.pdf
- 图片 -> 99_Attachments/papers/images/ego2robot/
- 索引已更新：05_Papers/index.md
```
