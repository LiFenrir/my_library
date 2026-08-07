---
title: paper-notes 迁移整理设计
description: 将旧论文仓库按 library 风格整理到 05_Papers 与 99_Attachments 的方案
tags: [design, migration, papers, knowledge-base]
created: 2026-07-15
---

# paper-notes 迁移整理设计

## 目标

将 `/home/kemove/INNOV/library/paper-notes/` 旧论文仓库按当前 `library/` 知识库风格重新整理，使论文 Markdown、原始 PDF、图片附件各归其位，人工笔记与 MinerU 转换原文可互相链接，最终删除冗余原目录。

## 现状

- `paper-notes/` 为 git 仓库克隆，含 5 个方向子目录
- 47 篇 Markdown：21 篇人工整理笔记（`论文笔记/*.md`），26 篇 MinerU 转换原文
- 22 个 PDF、151 张图片附件
- 笔记 frontmatter 不统一，部分缺 `description`、`created`
- 图片引用使用 `![[attachments/xxx.jpg]]`，附件为哈希或描述性命名

## 目标结构

```
library/
├── 05_Papers/
│   ├── index.md                 # 论文专区 MOC（由论文汇总.md 与 README.md 整理而来）
│   ├── notes/                   # 人工整理笔记（扁平）
│   │   ├── cosmos-policy.md
│   │   └── ...
│   └── articles/                # MinerU 转换原文（按方向分子目录）
│       ├── vla/
│       │   └── characterizing-vla-models/
│       │       └── characterizing-vla-models.md
│       ├── world-model/
│       ├── world-action-model/
│       ├── embodied-ai/
│       └── rl/
├── 99_Attachments/
│   ├── papers/
│   │   ├── pdfs/                # 原始 PDF
│   │   └── images/              # 论文图片（按论文 slug 分子目录）
│   │       └── cosmos-policy/
│   │           ├── cosmos-fig1-overview.jpg
│   │           └── ...
│   └── scripts/                 # 保留的 repair.py / repair_all.py
└── .docs/superpowers/specs/     # 本设计文档
```

## 映射规则

### 方向目录

| 原目录 | 目标 articles 子目录 | 标签 |
|---|---|---|
| VLA | `vla/` | VLA |
| 具身智能 | `embodied-ai/` | 具身智能 |
| 世界模型 | `world-model/` | 世界模型 |
| 世界动作模型 | `world-action-model/` | 世界动作模型 |
| 强化学习 | `rl/` | 强化学习 |

### 文件命名

- 全部转为**小写、短横线连接**的 Obsidian 风格 slug
- 示例：`Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.md` → `cosmos-policy.md`（notes）或 `cosmos-policy-fine-tuning-video-models-for-visuomotor-control-and-planning.md`（articles，与 PDF 同名）
- 保留必要区分：如 `LiteVLA_Edge` 与 `LiteVLA_H` 分别映射为 `litevla-edge`、`litevla-h`

### 论文 slug 映射（关键笔记）

| 原人工笔记 | 新 slug | 方向 |
|---|---|---|
| Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.md | cosmos-policy | world-model |
| Characterizing_VLA_Models.md | characterizing-vla-models | vla |
| pi0.7.md | pi0-7 | embodied-ai |
| piRL.md | pirl | vla |
| RISE.md | rise | embodied-ai |
| ARM.md | arm | embodied-ai |
| chi0.md | chi0 | embodied-ai |
| DexWorldModel.md | dexworldmodel | embodied-ai |
| GS-Playground_2604.25459.md | gs-playground | embodied-ai |
| LiteVLA_Edge.md | litevla-edge | vla |
| LiteVLA_H.md | litevla-h | vla |
| Motus_A_Unified_Latent_Action_World_Model.md | motus | world-model |
| Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination.md | fast-wam | world-action-model |
| World_Action_Models_are_Zero-shot_Policies.md | world-action-models-zero-shot | world-action-model |
| Privileged_Foresight_Distillation.md | privileged-foresight-distillation | world-model |
| Causal_World_Modeling_for_Robot_Control.md | causal-world-modeling | world-model |
| World_Models.md | world-models | world-model |
| A_Path_Towards_Autonomous_Machine_Intelligence.md | path-towards-autonomous-machine-intelligence | world-model |
| Recursive_Multi-Agent_Systems.md | recursive-multi-agent-systems | rl |
| RL_Token_Bootstrapping.md | rl-token-bootstrapping | vla |
| Tsallis_Loss_Continuum.md | tsallis-loss-continuum | rl |

## frontmatter 转换

人工整理笔记统一为 library 标准：

```yaml
---
title: "原 title"
description: "一句话概括论文核心贡献"
tags: [方向, 关键词1, 关键词2, ...]
created: 2026-07-15
---
```

- `authors`、`venue`、`year` 移至正文「基本信息」部分
- 缺 `description` 的笔记，按以下优先级生成 1 句话：
  1. 正文「主要研究成果」首句
  2. 摘要首句
  3. `title` + 核心方向/方法拼接
- 缺 `tags` 的 6 篇笔记，根据论文汇总.md 或正文关键词补充
- `created` 统一使用迁移日期 `2026-07-15`
- articles 文件保持原有 frontmatter（若有），仅添加 `created`

## 附件与 PDF 处理

### PDF

- 所有 `.pdf` 移动到 `99_Attachments/papers/pdfs/`
- 重命名为短横线小写 slug，与对应 article 同名
- 示例：`Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.pdf` → `cosmos-policy-fine-tuning-video-models-for-visuomotor-control-and-planning.pdf`

### 图片

- 所有 `论文笔记/attachments/` 图片移动到 `99_Attachments/papers/images/<slug>/`
- 描述性命名的图片保留原名并转小写/短横线
- 哈希命名的图片保留原名，避免链接断裂
- 多论文共用图片时，复制到各自 slug 目录

### 链接修复

- 笔记中 `![[attachments/xxx.jpg]]` 改为 `![[99_Attachments/papers/images/<slug>/xxx.jpg]]`
- 笔记中相对路径或绝对路径指向 PDF 的，改为指向 `99_Attachments/papers/pdfs/<slug>.pdf`
- 笔记中引用其他论文的 `[[旧文件名]]` 链接，更新为新 slug
- 在 notes 末尾增加「原文」链接：`[[05_Papers/articles/<方向>/<slug>/<slug>|<方向>/<slug>/<slug>]]`

## 重复与翻译文件处理

### 重复

同一篇论文在 notes、articles、PDF 中会同时存在，这是预期设计：
- `notes/`：人工整理、结构化的核心阅读入口
- `articles/`：MinerU 原始转换，供 agent 读取
- `pdfs/`：原始论文归档

### 中文翻译

- `具身智能/RISE_Self-Improving_Robot_Policy_with_Compositional_World_Model/RISE_中文翻译.md` 移动到 `05_Papers/articles/embodied-ai/rise/` 下，命名为 `rise-zh-translation.md`
- 与 `rise.md` 英文原文放在同一目录

## 保留文件

| 原路径 | 处理方式 |
|---|---|
| `paper-notes/script/repair.py` | 移动到 `99_Attachments/scripts/repair.py` |
| `paper-notes/script/repair_all.py` | 移动到 `99_Attachments/scripts/repair_all.py` |
| `paper-notes/README.md` | 内容合并到 `05_Papers/index.md` |
| `paper-notes/论文汇总.md` | 内容整理后作为 `05_Papers/index.md` 主体 |
| `paper-notes/.git` | 删除 |
| `paper-notes/CLAUDE.md` | 删除（内容已过时） |

## 废弃目录

迁移完成后删除 `paper-notes/` 整个目录。

## 实施步骤

1. 创建目标目录结构
2. 迁移 PDF 到 `99_Attachments/papers/pdfs/` 并重命名
3. 迁移图片到 `99_Attachments/papers/images/<slug>/`
4. 迁移并重命名 articles 到 `05_Papers/articles/<方向>/<slug>/`
5. 迁移并转换 notes 到 `05_Papers/notes/`
6. 修复所有图片和 PDF 链接
7. 生成 `05_Papers/index.md`
8. 迁移 repair.py 到 `99_Attachments/scripts/`
9. 删除 `paper-notes/` 目录
10. 验证：检查 frontmatter、链接、附件完整性

## 验证标准

- `05_Papers/notes/` 下 21 篇笔记均有完整 frontmatter
- `05_Papers/articles/` 下文件全部按方向子目录存放
- `99_Attachments/papers/pdfs/` 下 22 个 PDF 全部到位
- `99_Attachments/papers/images/` 下 151 张图片全部到位
- 所有 `![[...]]` 图片链接有效
- `05_Papers/index.md` 包含论文清单和双向链接
- `paper-notes/` 目录已删除
