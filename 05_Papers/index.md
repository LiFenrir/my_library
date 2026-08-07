---
title: "论文专区"
description: "论文精读与批注入口：人工笔记、MinerU 原文、按主题索引"
tags: [moc, papers]
created: 2026-07-15
---

# 论文专区

这里是个人论文知识资产入口。每篇论文沉淀为两类文件：

- **人工笔记** —— 放在 `05_Papers/notes/`，包含核心方法、工程价值判断、待验证问题。
- **MinerU 原文** —— 放在 `05_Papers/articles/`，保留 PDF 转换后的完整内容，供快速查找公式与实验细节。

原始 PDF 与图片统一归档在 `99_Attachments/papers/` 下。

## 子领域

- [[05_Papers/by-topic|按主题浏览]] — 网页论文专区首页（按研究方向分组卡片）
- VLA 与机器人策略
  - [[05_Papers/notes/characterizing-vla-models|characterizing-vla-models]]
  - [[05_Papers/notes/phail|phail]]
  - [[05_Papers/notes/pi-0-6|pi-0-6]]
  - [[05_Papers/notes/pi0-7|pi0-7]]
- World Model / World Action Model
  - [[05_Papers/notes/causal-world-modeling|causal-world-modeling]]
  - [[05_Papers/notes/cosmos-policy|cosmos-policy]]
  - [[05_Papers/notes/world-models|world-models]]

## 文件结构

- `05_Papers/notes/` — 人工整理笔记
- `05_Papers/articles/` — MinerU 转换原文（供 agent 读取）
- [[05_Papers/by-topic|按主题浏览]] — 手动维护的研究方向分组索引
- `99_Attachments/papers/images/` — 论文图片
- `99_Attachments/papers/pdfs/` — 原始 PDF

## 统计

- MinerU 原文：30 篇
- 人工笔记：29 篇

## 新增论文流程

1. 将 PDF 放入 `99_Attachments/papers/pdfs/`
2. 生成/复制 MinerU 原文到 `05_Papers/articles/<slug>.md`
3. 在 `05_Papers/notes/` 中撰写结构化笔记
4. 将图片放入 `99_Attachments/papers/images/<slug>/`

相关入口：
- [[02_AI/index|02_AI]] — 通用人工智能方法
- [[04_Embodied-AI/index|04_Embodied-AI]] — 具身智能
