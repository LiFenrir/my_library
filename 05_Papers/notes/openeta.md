---
title: "ETA: A New Agentic Paradigm for Embodied Tasks"
description: "将数字 Agent 的 Planner-Tool-Interface-World 闭环引入物理世界，用结构化命令、可信回执和可审计轨迹构建通用、可控、可自改进的具身任务 Agent。"
tags: ["embodied-ai", "robot-agent", "tool-use", "openeta", "LIBERO", "MCP"]
created: 2026-08-07
---

# ETA: A New Agentic Paradigm for Embodied Tasks

## 基本信息

- **作者**: Yitong Chen, Zezheng Huai, Sixian Li, Yubang Wang, Haozhe Zhang, Yifei Zhang, Hechang Chen, Jingjing Gong, Yu-Gang Jiang, Xipeng Qiu
- **机构**: Shanghai Innovation Institute, Fudan University, Jilin University, Nanjing University, Zhejiang University
- **链接**: [arXiv:2608.03924](https://arxiv.org/abs/2608.03924)
- **发表**: 2026-08-04
- **代码**: [OpenMOSS/OpenETA](https://github.com/OpenMOSS/OpenETA)
- **项目页**: [openmoss.ai/OpenETA](https://openmoss.ai/OpenETA/)
- **原文**: [[05_Papers/articles/openeta.md|openeta.md]]
- **PDF**: [[99_Attachments/papers/pdfs/openeta.pdf|openeta.pdf]]

## 研究背景

当前具身系统多为端到端 observation-to-action 模型（VLA / WAM），能力边界高度依赖机器人训练数据覆盖，长程任务难控制、难调试、难验证。作者认为具身智能的“ChatGPT 时刻”需要三类能力：

1. **通用性**：跨物体、环境、本体形态复用/组合感知、规划、控制能力。
2. **可控性**：在长程交互中维持显式任务状态，通过受限接口暴露动作，用实际执行结果决定下一步。
3. **自改进性**：把成功/失败交互转化为可复用经验，并在更新前验证。

## 核心方法

**ETA（Embodied Task Agent）** 把数字 Agent 的交互范式搬到物理世界：

```
Planner → Interface → World → (observation, receipt) → Planner
```

### 三个角色

- **Agent / Planner**：理解任务，维护工作记忆，每次只提出一个结构化命令（tool_call / response）。
- **Interface**：校验命令结构、权限、先决证据；负责 Tool 分发与执行门控；把异构后端（仿真/真机）统一为稳定 Tool 语义。
- **World**：通过 MCP 服务暴露仿真或真机能力，返回 Tool 结果、环境回执和新鲜观测。

### 运行时不变量

> 每次只执行一个会改变世界状态的动作；之后必须获取新的观测，才能做下一个依赖状态的动作。

该规则避免 Agent 基于过 stale 的图像连续假设世界状态，观测失败时安全停止而非猜测。

### OpenETA 系统

提供两类配置：

- **Full OpenETA**：44 个 Tool，覆盖感知定位、几何抓取规划、安全执行、环境证据、Agent 支持五大类。
- **OpenETA for Codex**：仅暴露 `observe`、`mark_point`、`move_to` 三个物理 Tool，验证“小接口 + 强 Planner”即可完成复杂操作。

关键机制：

- Tool 声明副作用类别：`read_only` / `planning` / `bookkeeping` / `world_mutating`，决定是否能批量调用及是否需要新鲜观测。
- 可信环境回执：reward / termination 只能由 host 背书，普通 Tool handler 无法伪造。
- 可重放轨迹：观测、命令、动作、回执、决策依据全部记录，便于审计、调试、复现。

## 实验设置

在 [[LIBERO]] 操作基准上评估，不使用任何 VLA 或任务专用策略作为 Tool。

### Full OpenETA

- 40 个任务 × 10 个种子 = 400 episodes
- Planner：GPT-5.6 Luna（medium reasoning）
- 仅使用 frozen evaluation manifest 中的配置

### OpenETA for Codex

- 130 个 LIBERO 任务：Spatial / Object / Goal / LIBERO-10 / LIBERO-90
- 比较 GPT-5.6 Luna、Terra、Sol
- 仅三个 Tool：observe、mark_point、move_to

## 主要结果

### Full OpenETA

| Suite | 成功率 |
|---|---|
| Spatial | 8.0% |
| Object | 26.0% |
| Goal | 21.0% |
| Long / LIBERO-10 | 1.0% |
| **Overall** | **14.0% (56/400)** |

失败以 `episode_timeout` 为主（62.5%），长程子目标跟踪、感知复检、放置关系、剩余预算协调是主要瓶颈。

### OpenETA for Codex

| Planner | PASS@1 | PASS@5 |
|---|---|---|
| GPT-5.6 Luna | 21/130 | 62/130 (47.7%) |
| GPT-5.6 Terra | 58/130 | 83/130 (63.8%) |
| GPT-5.6 Sol | 92/130 | **117/130 (90.0%)** |

在完全相同的 Tool 接口下，更强的 Planner 显著提升任务覆盖，说明接口设计能把“物理控制复杂度”与“Planner 能力”解耦。

### 受限自进化

测试了在线多轮 Skill、任务级 Skill、精确任务剧本、阶段级 delta 四类经验更新。**没有候选通过所有晋升门控**，验证了“经验必须经过配对非回归验证才能影响执行”这一机制设计，但当前方法尚未带来可复现的性能提升。

## 个人思考与启发

1. **范式对比**：VLA 是动作预测模型，WAM 是未来预测模型，ETA 是任务级协调 Agent。三者不是替代关系，未来 VLA/WAM 可作为 ETA 的 Tool 被调用。
2. **接口是核心资产**：OpenETA for Codex 证明，只要 Planner 够强，三个简单 Tool 就能完成大量 LIBERO 任务。这让我重新思考“机器人能力到底是模型问题还是接口问题”。
3. **信任链设计**：把 reward/termination 的背书权收回到 host，避免模型通过修改 prompt 或伪造反馈“作弊”，对 evaluation 非常关键。
4. **工程复现性**：frozen manifest + 可重放轨迹 + 官方回执，是物理 Agent 结果可信的基础。未来写实验时要考虑类似的 evidence chain。

## 局限与未来

- 长程子目标、放置关系、释放时机仍是瓶颈；
- timeout 和 budget 管理不足；
- 双手协调、动态接触、移动操作缺乏成熟 Tool；
- 真机目前只是接口级集成，尚未完成正式审计；
- 自进化尚未产生稳定增益，需要更精确地记录“规则触发—动作差异—结果因果”。

## 相关论文

- [[02_AI/LLM/ReAct|ReAct]]
- [[02_AI/LLM/Reflexion|Reflexion]]
- [[02_AI/Agent/Voyager|Voyager]]
- [[02_AI/VLM/RT-2|RT-2]]
- [[02_AI/VLM/OpenVLA|OpenVLA]]
- [[02_AI/LLM/World-Action-Model|World Action Models]]
- [[02_AI/VLM/CoRE-VLA|CoRE-VLA]]
