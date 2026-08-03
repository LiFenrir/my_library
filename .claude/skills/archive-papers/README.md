# archive-papers Skill

将 `library/00_Inbox/` 中的论文自动归档到 `05_Papers/`。

## 用法

在 library 项目内输入：

```
/archive-papers
```

可选参数：

- `/archive-papers --dry-run`：只预览，不移动文件。
- `/archive-papers --auto`：自动推断分类/slug，不逐篇询问。
- `/archive-papers --category vla`：强制指定分类。
- `/archive-papers --slug my-slug`：强制指定 slug（仅单篇时有效）。

## 自动化提醒

项目已配置 `SessionStart` hook。每次进入 library 项目时，如果 `00_Inbox/` 有待归档论文，会自动提示：

```
📥 检测到 00_Inbox 有 N 项待归档论文，可运行 /archive-papers 自动整理。
```

## 归档流程

1. 扫描 `00_Inbox/`，识别 `arxiv-*.pdf` 或已转换的 `arxiv-*/full.md` 目录。
2. 对仅有 PDF 的项调用 MinerU 转换为 markdown。
3. 读取原文，自动推断：标题、作者、分类、slug。
4. 生成 `05_Papers/notes/<slug>.md` 结构化笔记。
5. 移动文件到规范位置：
   - `05_Papers/articles/<slug>.md`
   - `99_Attachments/papers/pdfs/<slug>.pdf`
   - `99_Attachments/papers/images/<slug>/`
6. 更新 `05_Papers/index.md` 分类列表和统计数。

## 文件

- `SKILL.md`：Claude 执行指令。
- `scripts/archive_papers.py`：确定性文件操作脚本。
- `examples/phail.md`：归档示例。
