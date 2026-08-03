---
name: dedup-merge-conventions
description: 知识库去重合并的命名与操作规范:CamelCase 为主笔记、小写为待合并副本、合并后全局重写带路径链接
metadata:
  type: feedback
---

知识库重复笔记合并规范(2026-07-30 全库去重时确认):

- 主笔记取首字母大写驼峰式(如 `World-Model.md`);小写 kebab-case 文件多为后创建的重复副本。
- 各目录(`04_Embodied-AI/VLA`、`Robot-RL`、`02_AI`、`01_Fundamentals/ML`)既有命名习惯均以 CamelCase 为主。
- 内容差异小的同源重复:整合独有内容到主笔记,或在末尾追加 `## 补充:来自 [[主笔记|旧名(已合并)]]`;frontmatter 以主笔记为准。
- 删除旧文件前,必须全库重写 `[[带路径/旧名` 形式的链接(短链接 `[[stem]]` 由 Obsidian 按 stem 解析,无需改)。
- 跨目录重复(如 `01_Fundamentals/ML` 与 `04_Embodied-AI/Robot-RL` 同名概念):若内容同源(同一论文、同一公式),合并到 Fundamentals 规范位置,而非保留两份。

**Why:** 用户明确要求统一 CamelCase 命名并保留所有有效链接;2026-07-30 合并 18 对重复时按此执行,84 处链接重写无死链残留。

**How to apply:** 后续 [[knowledge-manager]] 归档或再次发现大小写重复对时,直接按此规范处理;合并类任务收尾必须跑一遍死链扫描验证。
