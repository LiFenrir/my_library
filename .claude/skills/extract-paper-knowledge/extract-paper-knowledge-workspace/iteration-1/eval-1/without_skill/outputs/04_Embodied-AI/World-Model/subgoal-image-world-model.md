---
title: "子目标图像世界模型"
description: "为 VLA 生成近未来子目标图像的轻量级世界模型：基于图像生成模型、条件流匹配、异步推理。"
tags: [embodied-ai, world-model, subgoal-image, vla]
created: 2026-07-28
---

# 子目标图像世界模型

子目标图像把抽象语言指令转化为具体视觉目标，帮助低层 VLA 理解“世界应该变成什么样”。

## 模型定义

- 输入：当前观测 $\mathbf{o}_t$、子任务指令 $\hat{\ell}_t$、episode metadata $m$。
- 输出：多视角近未来图像 $\mathbf{g}_t$。
- 训练目标：条件流匹配损失 $\mathcal{L}_{\mathrm{CFM}}(\mathbf{g}_t^\star, g_\psi(\mathbf{o}_t, \hat{\ell}_t, m))$。

## 实现要点

- **初始化**：从大规模图像生成/编辑模型（如 BAGEL）初始化，保留 web-scale 视觉语义。
- **训练数据**：高质量分段子任务标签的机器人数据、第一人称人类视频、开源图像编辑/视频数据集。
- **子目标采样**：
  - 25% 概率取段末真实帧（与世界模型训练目标一致）。
  - 75% 概率从当前时刻 0–4 秒未来均匀采样。
  - 额外加入模型生成的子目标图像，减少训练-测试分布差异。
- **推理策略**：当子任务变化或距上次生成超过 4 秒时重新生成；与 VLA 推理异步执行，保证低延迟。

## 作用

- 为语言指令提供视觉落地，改善语言跟随与空间推理。
- 在跨 embodiment 迁移中生成目标机器人视角下的合理视觉类比。

相关：
- [[04_Embodied-AI/VLA/multimodal-context-conditioning|VLA 的多模态上下文条件]] — 子目标图像在 prompt 中的位置
- [[04_Embodied-AI/generalization/cross-embodiment-transfer|跨 embodiment 迁移]] — 子目标图像对迁移的帮助
- [[05_Papers/articles/pi0-7|pi0.7 论文笔记]]
