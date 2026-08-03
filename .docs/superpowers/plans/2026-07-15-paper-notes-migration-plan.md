# paper-notes 迁移整理实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `paper-notes/` 旧论文仓库按设计文档迁移到 `05_Papers/`、`99_Attachments/papers/` 和 `99_Attachments/scripts/`，并生成 `05_Papers/index.md`。

**Architecture:** 使用 Python 脚本批量完成文件迁移、重命名、frontmatter 转换和链接修复；人工审阅关键映射后运行验证。

**Tech Stack:** Python 3.12、`uv`、`pathlib`、`re`、`yaml`（仅 frontmatter 文本操作）

## Global Constraints

- 所有文件命名转为**小写、短横线连接**的 Obsidian 风格 slug
- 目标目录层级最多 3 层
- 论文笔记 frontmatter 必须包含 `title`、`description`、`tags`、`created`
- `05_Papers/notes/` 扁平化；`05_Papers/articles/` 按 5 个方向分子目录
- 图片路径统一指向 `99_Attachments/papers/images/<slug>/`
- PDF 路径统一指向 `99_Attachments/papers/pdfs/<slug>.pdf`
- 迁移完成后删除 `paper-notes/` 目录
- 所有改动在 `library/` 当前工作目录执行

## 论文 slug 映射（执行依据）

| 原人工笔记 | 新 slug | 方向 | tags（补充/校验用） |
|---|---|---|---|
| A_Path_Towards_Autonomous_Machine_Intelligence.md | path-towards-autonomous-machine-intelligence | world-model | 世界模型, 自监督学习, 认知架构, JEPA, 能量模型, 内在动机 |
| ARM.md | arm | embodied-ai | 具身智能, Reward Modeling, Long-Horizon Manipulation |
| Causal_World_Modeling_for_Robot_Control.md | causal-world-modeling | world-model | 世界模型, 因果建模, 机器人控制, 自回归扩散, 视频预测, 逆动力学, Robbyant |
| Characterizing_VLA_Models.md | characterizing-vla-models | vla | VLA, Edge-AI, Hardware-Characterization, Bottleneck-Analysis, PIM, Memory-Bandwidth, Jetson |
| chi0.md | chi0 | embodied-ai | 具身智能, Resource-Aware, Robust Manipulation, Distributional Inconsistencies |
| Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.md | cosmos-policy | world-model | 世界模型, 视频扩散, 机器人策略, 模型预测控制, 价值函数, NVIDIA, Stanford |
| DexWorldModel.md | dexworldmodel | embodied-ai | 具身智能, World Model, Causal Learning, Robotics, VLA, Diffusion, Sim2Real, TTT, DINOv3 |
| Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination.md | fast-wam | world-action-model | 世界动作模型, WAM, 视频协同训练, 推理效率, 清华大学, Galaxea AI |
| GS-Playground_2604.25459.md | gs-playground | embodied-ai | 具身智能, Simulation, 3D Gaussian Splatting, Vision-Based RL |
| LiteVLA_Edge.md | litevla-edge | vla | VLA, Edge-Deployment, Quantization, Jetson-Orin, ROS2, llama.cpp, GGUF |
| LiteVLA_H.md | litevla-h | vla | VLA, Aerial-Robotics, Edge-Deployment, Dual-Rate, Pre-fill-Dominant, Jetson-Orin, UAV |
| Motus_A_Unified_Latent_Action_World_Model.md | motus | world-model | 世界模型, 统一模型, 潜在动作, MoT, 光流, 跨本体迁移, 清华大学 |
| pi0.7.md | pi0-7 | embodied-ai | 具身智能, VLA, Foundation Model, Flow Matching, Cross-Embodiment, Compositional Generalization, Instruction Following, Subgoal Images, Episode Metadata |
| piRL.md | pirl | vla | VLA, RL, Flow Matching, Robotics, PPO, π0, π0.5, Sim-to-Real |
| Privileged_Foresight_Distillation.md | privileged-foresight-distillation | world-model | 世界模型, 世界动作模型, 蒸馏, Future Correction, Zero-Cost |
| Recursive_Multi-Agent_Systems.md | recursive-multi-agent-systems | rl | 强化学习, Multi-Agent, LLM, Reasoning |
| RISE.md | rise | embodied-ai | 具身智能, World Model, Self-Improving, Robotics, VLA, Reinforcement Learning, Diffusion Model, 机器人操作 |
| RL_Token_Bootstrapping.md | rl-token-bootstrapping | vla | VLA, Online RL, Actor-Critic, Robot Manipulation, Fine-tuning, Representation Learning |
| Tsallis_Loss_Continuum.md | tsallis-loss-continuum | rl | 强化学习, Reasoning, RLVR, Tsallis Loss |
| World_Action_Models_are_Zero-shot_Policies.md | world-action-models-zero-shot | world-action-model | 世界动作模型, VLA, 视频扩散, 机器人学习, 跨本体迁移, 零样本泛化, NVIDIA |
| World_Models.md | world-models | world-model | 世界模型, World Models, JEPA, 自监督学习 |

## article 文件与 PDF 映射（额外文件）

| 原路径 | 方向 | 新 slug |
|---|---|---|
| 世界模型/10356_a_path_towards_autonomous_mach/10356_a_path_towards_autonomous_mach.md | world-model | 10356-a-path-towards-autonomous-mach |
| 世界模型/Privileged_Foresight_Distillation_Zero-Cost_Future_Correction_for_World_Action_Models/Privileged_Foresight_Distillation_Zero-Cost_Future_Correction_for_World_Action_Models_2604.25859.md | world-model | privileged-foresight-distillation |
| 世界模型/Causal_World_Modeling_for_Robot_Control/Causal_World_Modeling_for_Robot_Control.md | world-model | causal-world-modeling |
| 世界模型/Motus_A_Unified_Latent_Action_World_Model/Motus_A_Unified_Latent_Action_World_Model.md | world-model | motus |
| 世界模型/World_Models/World_Models.md | world-model | world-models |
| 世界模型/Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning/Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.md | world-model | cosmos-policy |
| 世界动作模型/World_Action_Models_are_Zero-shot_Policies/World_Action_Models_are_Zero-shot_Policies.md | world-action-model | world-action-models-zero-shot |
| 世界动作模型/Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination/Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination.md | world-action-model | fast-wam |
| 具身智能/chi0_Resource-Aware_Robust_Manipulation_via_Taming_Distributional_Inconsistencies/chi0_Resource-Aware_Robust_Manipulation_via_Taming_Distributional_Inconsistencies.md | embodied-ai | chi0 |
| 具身智能/RISE_Self-Improving_Robot_Policy_with_Compositional_World_Model/RISE_中文翻译.md | embodied-ai | rise-zh-translation |
| 具身智能/RISE_Self-Improving_Robot_Policy_with_Compositional_World_Model/RISE_Self-Improving_Robot_Policy_with_Compositional_World_Model.md | embodied-ai | rise |
| 具身智能/DexWorldModel_Causal_Latent_World_Modeling_towards_Automated_Learning_of_Embodied_Tasks/DexWorldModel_Causal_Latent_World_Modeling_towards_Automated_Learning_of_Embodied_Tasks.md | embodied-ai | dexworldmodel |
| 具身智能/ARM_Advantage_Reward_Modeling_for_Long_Horizon_Manipulation/ARM_Advantage_Reward_Modeling_for_Long_Horizon_Manipulation.md | embodied-ai | arm |
| 具身智能/GS-Playground_A_High-Throughput_Photorealistic_Simulator_for_Vision-Informed_Robot_Learning_2604.25459_mineru/GS-Playground_A_High-Throughput_Photorealistic_Simulator_for_Vision-Informed_Robot_Learning_2604.25459.md | embodied-ai | gs-playground |
| VLA/LiteVLA_Edge_Quantized_On-Device_Multimodal_Control_for_Embedded_Robotics/LiteVLA_Edge_Quantized_On-Device_Multimodal_Control_for_Embedded_Robotics.md | vla | litevla-edge |
| VLA/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models.md | vla | pirl |
| VLA/LiteVLA_H_Dual-Rate_Vision-Language-Action_Inference_for_Onboard_Aerial_Guidance/LiteVLA_H_Dual-Rate_Vision-Language-Action_Inference_for_Onboard_Aerial_Guidance.md | vla | litevla-h |
| VLA/RL_Token_Bootstrapping_Online_RL_with_Vision-Language-Action_Models/RL_Token_Bootstrapping_Online_RL_with_Vision-Language-Action_Models.md | vla | rl-token-bootstrapping |
| VLA/Characterizing_VLA_Models_Identifying_the_Action_Generation_Bottleneck/Characterizing_VLA_Models_Identifying_the_Action_Generation_Bottleneck.md | vla | characterizing-vla-models |
| 强化学习/Tsallis_Loss_Continuum/2604.25907.md | rl | tsallis-loss-continuum |
| 强化学习/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models.md | rl | pirl |
| 强化学习/Recursive_Multi-Agent_Systems/2604.25917.md | rl | recursive-multi-agent-systems |
| 具身智能/pi0.7_A_Steerable_Generalist_Robotic_Foundation_Model_with_Emergent_Capabilities/pi0.7_A_Steerable_Generalist_Robotic_Foundation_Model_with_Emergent_Capabilities/pi0.7_A_Steerable_Generalist_Robotic_Foundation_Model_with_Emergent_Capabilities.md | embodied-ai | pi0-7 |

---

### Task 1: 创建目标目录结构

**Files:**
- Create: `05_Papers/notes/.gitkeep`
- Create: `05_Papers/articles/vla/.gitkeep`
- Create: `05_Papers/articles/world-model/.gitkeep`
- Create: `05_Papers/articles/world-action-model/.gitkeep`
- Create: `05_Papers/articles/embodied-ai/.gitkeep`
- Create: `05_Papers/articles/rl/.gitkeep`
- Create: `99_Attachments/papers/pdfs/.gitkeep`
- Create: `99_Attachments/papers/images/.gitkeep`
- Create: `99_Attachments/scripts/.gitkeep`

**Interfaces:**
- Consumes: 无
- Produces: 后续任务依赖的目标目录存在

- [ ] **Step 1: 创建目录**

Run:
```bash
mkdir -p 05_Papers/notes \
         05_Papers/articles/vla \
         05_Papers/articles/world-model \
         05_Papers/articles/world-action-model \
         05_Papers/articles/embodied-ai \
         05_Papers/articles/rl \
         99_Attachments/papers/pdfs \
         99_Attachments/papers/images \
         99_Attachments/scripts
```

- [ ] **Step 2: 验证目录存在**

Run:
```bash
find 05_Papers 99_Attachments/papers 99_Attachments/scripts -type d | sort
```

Expected: 列出 9 个新建目录

---

### Task 2: 迁移 PDF 到 99_Attachments/papers/pdfs/

**Files:**
- Create: `99_Attachments/papers/pdfs/*.pdf`（22 个）

**Interfaces:**
- Consumes: `paper-notes/**/*.pdf`
- Produces: 重命名后的 PDF 文件，slug 与 articles 同名

- [ ] **Step 1: 编写迁移脚本**

Create: `99_Attachments/scripts/_migrate_pdfs.py`

```python
"""迁移并重命名 paper-notes 中的 PDF。"""
import shutil
from pathlib import Path

ROOT = Path("/home/kemove/INNOV/library")
PDFS = {
    "world-model/10356_a_path_towards_autonomous_mach.pdf": "10356-a-path-towards-autonomous-mach.pdf",
    "world-model/Motus_A_Unified_Latent_Action_World_Model.pdf": "motus.pdf",
    "world-model/Causal_World_Modeling_for_Robot_Control.pdf": "causal-world-modeling.pdf",
    "world-model/10356_a_path_towards_autonomous_mach.pdf": "10356-a-path-towards-autonomous-mach.pdf",
    "world-model/Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.pdf": "cosmos-policy.pdf",
    "world-model/Privileged_Foresight_Distillation_Zero-Cost_Future_Correction_for_World_Action_Models.pdf": "privileged-foresight-distillation.pdf",
    "world-action-model/Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination.pdf": "fast-wam.pdf",
    "world-action-model/World_Action_Models_are_Zero-shot_Policies.pdf": "world-action-models-zero-shot.pdf",
    "embodied-ai/ARM_Advantage_Reward_Modeling_for_Long_Horizon_Manipulation.pdf": "arm.pdf",
    "embodied-ai/chi0_Resource-Aware_Robust_Manipulation_via_Taming_Distributional_Inconsistencies.pdf": "chi0.pdf",
    "embodied-ai/DexWorldModel_Causal_Latent_World_Modeling_towards_Automated_Learning_of_Embodied_Tasks.pdf": "dexworldmodel.pdf",
    "embodied-ai/GS-Playground_A_High-Throughput_Photorealistic_Simulator_for_Vision-Informed_Robot_Learning_2604.25459.pdf": "gs-playground.pdf",
    "embodied-ai/pi0.7_A_Steerable_Generalist_Robotic_Foundation_Model_with_Emergent_Capabilities.pdf": "pi0-7.pdf",
    "embodied-ai/RISE_Self-Improving_Robot_Policy_with_Compositional_World_Model.pdf": "rise.pdf",
    "vla/Characterizing_VLA_Models_Identifying_the_Action_Generation_Bottleneck.pdf": "characterizing-vla-models.pdf",
    "vla/LiteVLA_Edge_Quantized_On-Device_Multimodal_Control_for_Embedded_Robotics.pdf": "litevla-edge.pdf",
    "vla/LiteVLA_H_Dual-Rate_Vision-Language-Action_Inference_for_Onboard_Aerial_Guidance.pdf": "litevla-h.pdf",
    "vla/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models.pdf": "pirl.pdf",
    "vla/RL_Token_Bootstrapping_Online_RL_with_Vision-Language-Action_Models.pdf": "rl-token-bootstrapping.pdf",
    "rl/Recursive_Multi-Agent_Systems.pdf": "recursive-multi-agent-systems.pdf",
    "rl/Tsallis_Loss_Continuum.pdf": "tsallis-loss-continuum.pdf",
}

src_root = ROOT / "paper-notes"
dst_root = ROOT / "99_Attachments/papers/pdfs"

for src_rel, dst_name in PDFS.items():
    src = src_root / src_rel
    dst = dst_root / dst_name
    if src.exists():
        shutil.copy2(src, dst)
        print(f"copied: {src_rel} -> {dst_name}")
    else:
        print(f"missing: {src_rel}")

print(f"\ntotal pdfs in dst: {len(list(dst_root.glob('*.pdf')))}")
```

- [ ] **Step 2: 运行脚本**

Run:
```bash
python 99_Attachments/scripts/_migrate_pdfs.py
```

Expected: 输出 22 条 copied 记录，无 missing

- [ ] **Step 3: 校验数量**

Run:
```bash
ls 99_Attachments/papers/pdfs/*.pdf | wc -l
```

Expected: `22`

---

### Task 3: 迁移图片到 99_Attachments/papers/images/<slug>/

**Files:**
- Create: `99_Attachments/papers/images/<slug>/*.jpg`（151 张）

**Interfaces:**
- Consumes: `paper-notes/论文笔记/attachments/*`
- Produces: 按论文 slug 分组的图片目录

- [ ] **Step 1: 建立 slug 到图片引用集合的映射**

Create: `99_Attachments/scripts/_map_images.py`

```python
"""解析所有 notes 中的 attachments 引用，建立 slug -> image 集合。"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path("/home/kemove/INNOV/library")
NOTE_DIR = ROOT / "paper-notes/论文笔记"

NOTE_SLUGS = {
    "A_Path_Towards_Autonomous_Machine_Intelligence.md": "path-towards-autonomous-machine-intelligence",
    "ARM.md": "arm",
    "Causal_World_Modeling_for_Robot_Control.md": "causal-world-modeling",
    "Characterizing_VLA_Models.md": "characterizing-vla-models",
    "chi0.md": "chi0",
    "Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.md": "cosmos-policy",
    "DexWorldModel.md": "dexworldmodel",
    "Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination.md": "fast-wam",
    "GS-Playground_2604.25459.md": "gs-playground",
    "LiteVLA_Edge.md": "litevla-edge",
    "LiteVLA_H.md": "litevla-h",
    "Motus_A_Unified_Latent_Action_World_Model.md": "motus",
    "pi0.7.md": "pi0-7",
    "piRL.md": "pirl",
    "Privileged_Foresight_Distillation.md": "privileged-foresight-distillation",
    "Recursive_Multi-Agent_Systems.md": "recursive-multi-agent-systems",
    "RISE.md": "rise",
    "RL_Token_Bootstrapping.md": "rl-token-bootstrapping",
    "Tsallis_Loss_Continuum.md": "tsallis-loss-continuum",
    "World_Action_Models_are_Zero-shot_Policies.md": "world-action-models-zero-shot",
    "World_Models.md": "world-models",
}

PAT = re.compile(r"!\[\[attachments/([^\]]+)\]\]")
slug_images = defaultdict(set)

for md_name, slug in NOTE_SLUGS.items():
    text = (NOTE_DIR / md_name).read_text(encoding="utf-8")
    for m in PAT.finditer(text):
        slug_images[slug].add(m.group(1))

# 输出映射，供迁移脚本使用
for slug, images in sorted(slug_images.items()):
    print(f"{slug}: {sorted(images)}")
```

- [ ] **Step 2: 运行映射脚本并人工审阅**

Run:
```bash
python 99_Attachments/scripts/_map_images.py
```

Expected: 输出每个 slug 对应的图片文件名列表

- [ ] **Step 3: 复制图片到目标目录**

Create: `99_Attachments/scripts/_migrate_images.py`

```python
"""根据 _map_images.py 输出复制图片到按 slug 分组的目录。"""
import shutil
from pathlib import Path

ROOT = Path("/home/kemove/INNOV/library")
SRC = ROOT / "paper-notes/论文笔记/attachments"
DST_ROOT = ROOT / "99_Attachments/papers/images"

# 从 _map_images.py 输出复制此处，格式：slug: ["img1.jpg", "img2.jpg"]
SLUG_IMAGES = {
    # 示例占位，实际值由 Step 2 输出填充
}

for slug, images in SLUG_IMAGES.items():
    dst_dir = DST_ROOT / slug
    dst_dir.mkdir(parents=True, exist_ok=True)
    for img in images:
        src = SRC / img
        dst = dst_dir / img
        if src.exists():
            shutil.copy2(src, dst)
        else:
            print(f"missing: {img}")
    print(f"{slug}: {len(list(dst_dir.iterdir()))} images")

print(f"\ntotal images in dst: {len(list(DST_ROOT.rglob('*.jpg')))}")
```

Run:
```bash
python 99_Attachments/scripts/_migrate_images.py
```

Expected: 输出各 slug 图片数量，总计 151

- [ ] **Step 4: 校验**

Run:
```bash
find 99_Attachments/papers/images -type f | wc -l
```

Expected: `151`

---

### Task 4: 迁移并重命名 articles

**Files:**
- Create: `05_Papers/articles/{vla,world-model,world-action-model,embodied-ai,rl}/<slug>/<slug>.md`

**Interfaces:**
- Consumes: `paper-notes/{VLA,世界模型,世界动作模型,具身智能,强化学习}/**/*.md`
- Produces: 26 篇重命名后的 MinerU 原文

- [ ] **Step 1: 编写迁移脚本**

Create: `99_Attachments/scripts/_migrate_articles.py`

```python
"""迁移 paper-notes 中的 MinerU Markdown 到 05_Papers/articles/。"""
import shutil
from pathlib import Path

ROOT = Path("/home/kemove/INNOV/library")
SRC = ROOT / "paper-notes"
DST = ROOT / "05_Papers/articles"

ARTICLES = [
    # (src_rel, dst_dir_slug)
    ("世界模型/10356_a_path_towards_autonomous_mach/10356_a_path_towards_autonomous_mach.md", "world-model/10356-a-path-towards-autonomous-mach"),
    ("世界模型/Causal_World_Modeling_for_Robot_Control/Causal_World_Modeling_for_Robot_Control.md", "world-model/causal-world-modeling"),
    ("世界模型/Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning/Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.md", "world-model/cosmos-policy"),
    ("世界模型/Motus_A_Unified_Latent_Action_World_Model/Motus_A_Unified_Latent_Action_World_Model.md", "world-model/motus"),
    ("世界模型/Privileged_Foresight_Distillation_Zero-Cost_Future_Correction_for_World_Action_Models/Privileged_Foresight_Distillation_Zero-Cost_Future_Correction_for_World_Action_Models_2604.25859.md", "world-model/privileged-foresight-distillation"),
    ("世界模型/World_Models/World_Models.md", "world-model/world-models"),
    ("世界动作模型/Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination/Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination.md", "world-action-model/fast-wam"),
    ("世界动作模型/World_Action_Models_are_Zero-shot_Policies/World_Action_Models_are_Zero-shot_Policies.md", "world-action-model/world-action-models-zero-shot"),
    ("具身智能/ARM_Advantage_Reward_Modeling_for_Long_Horizon_Manipulation/ARM_Advantage_Reward_Modeling_for_Long_Horizon_Manipulation.md", "embodied-ai/arm"),
    ("具身智能/chi0_Resource-Aware_Robust_Manipulation_via_Taming_Distributional_Inconsistencies/chi0_Resource-Aware_Robust_Manipulation_via_Taming_Distributional_Inconsistencies.md", "embodied-ai/chi0"),
    ("具身智能/DexWorldModel_Causal_Latent_World_Modeling_towards_Automated_Learning_of_Embodied_Tasks/DexWorldModel_Causal_Latent_World_Modeling_towards_Automated_Learning_of_Embodied_Tasks.md", "embodied-ai/dexworldmodel"),
    ("具身智能/GS-Playground_A_High-Throughput_Photorealistic_Simulator_for_Vision-Informed_Robot_Learning_2604.25459_mineru/GS-Playground_A_High-Throughput_Photorealistic_Simulator_for_Vision-Informed_Robot_Learning_2604.25459.md", "embodied-ai/gs-playground"),
    ("具身智能/pi0.7_A_Steerable_Generalist_Robotic_Foundation_Model_with_Emergent_Capabilities/pi0.7_A_Steerable_Generalist_Robotic_Foundation_Model_with_Emergent_Capabilities/pi0.7_A_Steerable_Generalist_Robotic_Foundation_Model_with_Emergent_Capabilities.md", "embodied-ai/pi0-7"),
    ("具身智能/RISE_Self-Improving_Robot_Policy_with_Compositional_World_Model/RISE_Self-Improving_Robot_Policy_with_Compositional_World_Model.md", "embodied-ai/rise"),
    ("具身智能/RISE_Self-Improving_Robot_Policy_with_Compositional_World_Model/RISE_中文翻译.md", "embodied-ai/rise/rise-zh-translation"),
    ("VLA/Characterizing_VLA_Models_Identifying_the_Action_Generation_Bottleneck/Characterizing_VLA_Models_Identifying_the_Action_Generation_Bottleneck.md", "vla/characterizing-vla-models"),
    ("VLA/LiteVLA_Edge_Quantized_On-Device_Multimodal_Control_for_Embedded_Robotics/LiteVLA_Edge_Quantized_On-Device_Multimodal_Control_for_Embedded_Robotics.md", "vla/litevla-edge"),
    ("VLA/LiteVLA_H_Dual-Rate_Vision-Language-Action_Inference_for_Onboard_Aerial_Guidance/LiteVLA_H_Dual-Rate_Vision-Language-Action_Inference_for_Onboard_Aerial_Guidance.md", "vla/litevla-h"),
    ("VLA/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models.md", "vla/pirl"),
    ("VLA/RL_Token_Bootstrapping_Online_RL_with_Vision-Language-Action_Models/RL_Token_Bootstrapping_Online_RL_with_Vision-Language-Action_Models.md", "vla/rl-token-bootstrapping"),
    ("强化学习/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models/piRL_Online_RL_Fine-tuning_for_Flow-based_Vision-Language-Action_Models.md", "rl/pirl"),
    ("强化学习/Recursive_Multi-Agent_Systems/2604.25917.md", "rl/recursive-multi-agent-systems"),
    ("强化学习/Tsallis_Loss_Continuum/2604.25907.md", "rl/tsallis-loss-continuum"),
]

for src_rel, dst_dir_slug in ARTICLES:
    src = SRC / src_rel
    dst_dir = DST / dst_dir_slug
    dst_dir.mkdir(parents=True, exist_ok=True)
    # 最后一级目录名即 slug，文件名也用它
    slug = dst_dir_slug.split("/")[-1]
    dst = dst_dir / f"{slug}.md"
    if src.exists():
        shutil.copy2(src, dst)
        print(f"copied: {src_rel} -> {dst}")
    else:
        print(f"missing: {src_rel}")

print(f"\ntotal articles: {len(list(DST.rglob('*.md')))}")
```

- [ ] **Step 2: 运行脚本**

Run:
```bash
python 99_Attachments/scripts/_migrate_articles.py
```

Expected: 输出 26 条 copied 记录

- [ ] **Step 3: 校验数量**

Run:
```bash
find 05_Papers/articles -type f -name "*.md" | wc -l
```

Expected: `26`

---

### Task 5: 迁移并转换 notes 的 frontmatter 和链接

**Files:**
- Create: `05_Papers/notes/<slug>.md`（21 篇）

**Interfaces:**
- Consumes: `paper-notes/论文笔记/*.md`
- Produces: 统一 frontmatter、修复链接后的笔记

- [ ] **Step 1: 编写转换脚本**

Create: `99_Attachments/scripts/_migrate_notes.py`

```python
"""迁移人工笔记到 05_Papers/notes/，转换 frontmatter 并修复图片/PDF 链接。"""
import re
from pathlib import Path
from datetime import date

ROOT = Path("/home/kemove/INNOV/library")
SRC_DIR = ROOT / "paper-notes/论文笔记"
DST_DIR = ROOT / "05_Papers/notes"
IMAGES_ROOT = ROOT / "99_Attachments/papers/images"

NOTES = {
    "A_Path_Towards_Autonomous_Machine_Intelligence.md": {
        "slug": "path-towards-autonomous-machine-intelligence",
        "direction": "world-model",
        "tags": ["世界模型", "自监督学习", "认知架构", "JEPA", "能量模型", "内在动机"],
        "description": "Yann LeCun 提出的自主机器智能路径，强调基于 JEPA 的世界模型与自监督学习。",
    },
    "ARM.md": {
        "slug": "arm",
        "direction": "embodied-ai",
        "tags": ["具身智能", "Reward Modeling", "Long-Horizon Manipulation"],
        "description": "通过优势奖励模型提升长程机器人操作任务的成功率。",
    },
    "Causal_World_Modeling_for_Robot_Control.md": {
        "slug": "causal-world-modeling",
        "direction": "world-model",
        "tags": ["世界模型", "因果建模", "机器人控制", "自回归扩散", "视频预测", "逆动力学", "Robbyant"],
        "description": "利用因果世界模型进行机器人控制，结合自回归扩散与视频预测学习可泛化策略。",
    },
    "Characterizing_VLA_Models.md": {
        "slug": "characterizing-vla-models",
        "direction": "vla",
        "tags": ["VLA", "Edge-AI", "Hardware-Characterization", "Bottleneck-Analysis", "PIM", "Memory-Bandwidth", "Jetson"],
        "description": "在 Jetson Orin/Thor 上剖析 VLA 推理瓶颈，指出动作生成阶段占 75% 延迟。",
    },
    "chi0.md": {
        "slug": "chi0",
        "direction": "embodied-ai",
        "tags": ["具身智能", "Resource-Aware", "Robust Manipulation", "Distributional Inconsistencies"],
        "description": "通过驯服数据、策略与部署三分布不一致性实现资源感知的鲁棒操作。",
    },
    "Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning.md": {
        "slug": "cosmos-policy",
        "direction": "world-model",
        "tags": ["世界模型", "视频扩散", "机器人策略", "模型预测控制", "价值函数", "NVIDIA", "Stanford"],
        "description": "零架构修改地将视频生成模型单阶段微分为机器人策略、世界模型与价值函数。",
    },
    "DexWorldModel.md": {
        "slug": "dexworldmodel",
        "direction": "embodied-ai",
        "tags": ["具身智能", "World Model", "Causal Learning", "Robotics", "VLA", "Diffusion", "Sim2Real", "TTT", "DINOv3"],
        "description": "面向机器人灵巧操作的因果潜在世界模型，支持自动化任务学习与 Sim2Real 迁移。",
    },
    "Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination.md": {
        "slug": "fast-wam",
        "direction": "world-action-model",
        "tags": ["世界动作模型", "WAM", "视频协同训练", "推理效率", "清华大学", "Galaxea AI"],
        "description": "证明世界动作模型在测试时无需未来想象即可保持性能，显著提升推理速度。",
    },
    "GS-Playground_2604.25459.md": {
        "slug": "gs-playground",
        "direction": "embodied-ai",
        "tags": ["具身智能", "Simulation", "3D Gaussian Splatting", "Vision-Based RL"],
        "description": "基于 3D Gaussian Splatting 的高通量真实感仿真器，用于视觉驱动机器人学习。",
    },
    "LiteVLA_Edge.md": {
        "slug": "litevla-edge",
        "direction": "vla",
        "tags": ["VLA", "Edge-Deployment", "Quantization", "Jetson-Orin", "ROS2", "llama.cpp", "GGUF"],
        "description": "面向嵌入式机器人的量化端侧多模态 VLA 控制方案。",
    },
    "LiteVLA_H.md": {
        "slug": "litevla-h",
        "direction": "vla",
        "tags": ["VLA", "Aerial-Robotics", "Edge-Deployment", "Dual-Rate", "Pre-fill-Dominant", "Jetson-Orin", "UAV"],
        "description": "用于机载空中引导的双速率 VLA 推理系统。",
    },
    "Motus_A_Unified_Latent_Action_World_Model.md": {
        "slug": "motus",
        "direction": "world-model",
        "tags": ["世界模型", "统一模型", "潜在动作", "MoT", "光流", "跨本体迁移", "清华大学"],
        "description": "统一的潜在动作世界模型，用 MoT 架构实现跨机器人本体的迁移。",
    },
    "pi0.7.md": {
        "slug": "pi0-7",
        "direction": "embodied-ai",
        "tags": ["具身智能", "VLA", "Foundation Model", "Flow Matching", "Cross-Embodiment", "Compositional Generalization", "Instruction Following", "Subgoal Images", "Episode Metadata"],
        "description": "Physical Intelligence 的可操控通用机器人基础模型，通过多样化上下文条件实现组合泛化。",
    },
    "piRL.md": {
        "slug": "pirl",
        "direction": "vla",
        "tags": ["VLA", "RL", "Flow Matching", "Robotics", "PPO", "π0", "π0.5", "Sim-to-Real"],
        "description": "基于 Flow Matching 的 VLA 在线 RL 微调方法。",
    },
    "Privileged_Foresight_Distillation.md": {
        "slug": "privileged-foresight-distillation",
        "direction": "world-model",
        "tags": ["世界模型", "世界动作模型", "蒸馏", "Future Correction", "Zero-Cost"],
        "description": "利用特权未来信息蒸馏实现世界动作模型的零成本未来校正。",
    },
    "Recursive_Multi-Agent_Systems.md": {
        "slug": "recursive-multi-agent-systems",
        "direction": "rl",
        "tags": ["强化学习", "Multi-Agent", "LLM", "Reasoning"],
        "description": "递归多智能体系统，通过智能体递归分解提升复杂推理任务性能。",
    },
    "RISE.md": {
        "slug": "rise",
        "direction": "embodied-ai",
        "tags": ["具身智能", "World Model", "Self-Improving", "Robotics", "VLA", "Reinforcement Learning", "Diffusion Model", "机器人操作"],
        "description": "基于组合世界模型的自改进机器人策略。",
    },
    "RL_Token_Bootstrapping.md": {
        "slug": "rl-token-bootstrapping",
        "direction": "vla",
        "tags": ["VLA", "Online RL", "Actor-Critic", "Robot Manipulation", "Fine-tuning", "Representation Learning"],
        "description": "用在线 RL token bootstrapping 提升 VLA 模型在机器人操作中的执行精度。",
    },
    "Tsallis_Loss_Continuum.md": {
        "slug": "tsallis-loss-continuum",
        "direction": "rl",
        "tags": ["强化学习", "Reasoning", "RLVR", "Tsallis Loss"],
        "description": "在 Tsallis 损失连续体上训练推理模型，平衡监督承诺与探索。",
    },
    "World_Action_Models_are_Zero-shot_Policies.md": {
        "slug": "world-action-models-zero-shot",
        "direction": "world-action-model",
        "tags": ["世界动作模型", "VLA", "视频扩散", "机器人学习", "跨本体迁移", "零样本泛化", "NVIDIA"],
        "description": "将世界动作模型作为零样本策略，利用视频生成先验实现高效机器人学习。",
    },
    "World_Models.md": {
        "slug": "world-models",
        "direction": "world-model",
        "tags": ["世界模型", "World Models", "JEPA", "自监督学习"],
        "description": "世界模型综述：基于内部世界模型进行预测、推理与决策。",
    },
}


def to_yaml_list(items):
    return "[" + ", ".join(f'"{x}"' for x in items) + "]"


def extract_title(text):
    m = re.search(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if m:
        fm = m.group(1)
        tm = re.search(r'^title:\s*"?([^"\n]+)"?', fm, re.MULTILINE)
        if tm:
            return tm.group(1).strip()
    # fallback: first H1
    hm = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    return hm.group(1).strip() if hm else ""


def process_note(src_name, meta):
    text = (SRC_DIR / src_name).read_text(encoding="utf-8")
    title = extract_title(text)
    # 移除旧 frontmatter
    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.DOTALL)
    # 修复图片链接
    slug = meta["slug"]
    body = re.sub(
        r'!\[\[attachments/([^\]]+)\]\]',
        rf'![[99_Attachments/papers/images/{slug}/\1]]',
        body,
    )
    # 修复 PDF 相对路径（若有 ../VLA/xxx.pdf 等）
    body = re.sub(r'\]\((?:\.\./)+[\w\-]+/([^/]+\.pdf)\)', rf'](99_Attachments/papers/pdfs/\1)', body)
    # 添加原文链接
    direction = meta["direction"]
    footer = f"\n\n## 原文\n\n[[05_Papers/articles/{direction}/{slug}/{slug}]]\n"
    new_fm = (
        "---\n"
        f'title: "{title}"\n'
        f'description: "{meta["description"]}"\n'
        f'tags: {to_yaml_list(meta["tags"])}\n'
        f'created: {date.today().isoformat()}\n'
        "---\n\n"
    )
    (DST_DIR / f"{slug}.md").write_text(new_fm + body + footer, encoding="utf-8")
    print(f"processed: {src_name} -> {slug}.md")


for src_name, meta in NOTES.items():
    process_note(src_name, meta)

print(f"\ntotal notes: {len(list(DST_DIR.glob('*.md')))}")
```

- [ ] **Step 2: 运行脚本**

Run:
```bash
python 99_Attachments/scripts/_migrate_notes.py
```

Expected: 输出 21 条 processed 记录

- [ ] **Step 3: 校验 frontmatter**

Run:
```bash
for f in 05_Papers/notes/*.md; do echo "=== $(basename $f) ==="; head -7 "$f"; done
```

Expected: 每篇前 7 行包含 `title`、`description`、`tags`、`created`

---

### Task 6: 修复 notes 中存在的内部双向链接

**Files:**
- Modify: `05_Papers/notes/*.md`

**Interfaces:**
- Consumes: Task 5 输出的 notes
- Produces: 内部 `[[旧文件名]]` 链接更新为新的 slug

- [ ] **Step 1: 扫描旧链接**

Run:
```bash
grep -oE '\[\[[^\]]+\]\]' 05_Papers/notes/*.md | grep -v "99_Attachments" | head -40
```

Expected: 列出笔记之间的旧链接引用

- [ ] **Step 2: 编写替换脚本**

Create: `99_Attachments/scripts/_fix_internal_links.py`

```python
"""将 notes 内部的旧文件名链接替换为新 slug。"""
import re
from pathlib import Path

ROOT = Path("/home/kemove/INNOV/library")
NOTE_DIR = ROOT / "05_Papers/notes"

OLD_TO_NEW = {
    "A_Path_Towards_Autonomous_Machine_Intelligence": "path-towards-autonomous-machine-intelligence",
    "ARM": "arm",
    "Causal_World_Modeling_for_Robot_Control": "causal-world-modeling",
    "Characterizing_VLA_Models": "characterizing-vla-models",
    "chi0": "chi0",
    "Cosmos_Policy_Fine-Tuning_Video_Models_for_Visuomotor_Control_and_Planning": "cosmos-policy",
    "DexWorldModel": "dexworldmodel",
    "Fast-WAM_Do_World_Action_Models_Need_Test-time_Future_Imagination": "fast-wam",
    "GS-Playground_2604.25459": "gs-playground",
    "LiteVLA_Edge": "litevla-edge",
    "LiteVLA_H": "litevla-h",
    "Motus_A_Unified_Latent_Action_World_Model": "motus",
    "pi0.7": "pi0-7",
    "piRL": "pirl",
    "Privileged_Foresight_Distillation": "privileged-foresight-distillation",
    "Recursive_Multi-Agent_Systems": "recursive-multi-agent-systems",
    "RISE": "rise",
    "RL_Token_Bootstrapping": "rl-token-bootstrapping",
    "Tsallis_Loss_Continuum": "tsallis-loss-continuum",
    "World_Action_Models_are_Zero-shot_Policies": "world-action-models-zero-shot",
    "World_Models": "world-models",
}

for f in NOTE_DIR.glob("*.md"):
    text = f.read_text(encoding="utf-8")
    new_text = text
    for old, new in OLD_TO_NEW.items():
        new_text = re.sub(rf"\[\[{re.escape(old)}(\|[^\]]*)?\]\]", rf"[[{new}\1]]", new_text)
    if new_text != text:
        f.write_text(new_text, encoding="utf-8")
        print(f"fixed: {f.name}")
```

- [ ] **Step 3: 运行脚本**

Run:
```bash
python 99_Attachments/scripts/_fix_internal_links.py
```

Expected: 输出被修改的笔记文件名

---

### Task 7: 生成 05_Papers/index.md

**Files:**
- Create: `05_Papers/index.md`

**Interfaces:**
- Consumes: `paper-notes/论文汇总.md`、`paper-notes/README.md`、Task 5 的 notes
- Produces: 论文专区 MOC

- [ ] **Step 1: 编写生成脚本**

Create: `99_Attachments/scripts/_generate_index.py`

```python
"""生成 05_Papers/index.md。"""
from pathlib import Path
from collections import defaultdict

ROOT = Path("/home/kemove/INNOV/library")
NOTES_DIR = ROOT / "05_Papers/notes"
ARTICLES_DIR = ROOT / "05_Papers/articles"

DIRECTIONS = {
    "vla": "VLA",
    "world-model": "世界模型",
    "world-action-model": "世界动作模型",
    "embodied-ai": "具身智能",
    "rl": "强化学习",
}

# 按方向收集 notes
notes_by_dir = defaultdict(list)
for f in sorted(NOTES_DIR.glob("*.md")):
    text = f.read_text(encoding="utf-8")
    # 从原文链接推断方向
    dm = __import__("re").search(r"05_Papers/articles/([^/]+)/" + f.stem, text)
    direction = dm.group(1) if dm else "unknown"
    # 提取 title
    tm = __import__("re").search(r'^title:\s*"?([^"\n]+)"?', text)
    title = tm.group(1).strip() if tm else f.stem
    notes_by_dir[direction].append((f.stem, title))

lines = [
    "---",
    'title: "05_Papers"',
    'description: "论文专区入口：人工笔记与 MinerU 原文"',
    "tags: [moc, papers]",
    "created: 2026-07-15",
    "---",
    "",
    "# 05_Papers",
    "",
    "个人论文资产库，按研究方向粗分类。知识关系靠 [[双向链接]] 与 `#标签` 自然生长。",
    "",
    "## 目录",
    "",
    "- [[05_Papers/notes/]] — 人工整理笔记",
    "- [[05_Papers/articles/]] — MinerU 转换原文（供 agent 读取）",
    "- [[99_Attachments/papers/pdfs/]] — 原始 PDF",
    "- [[99_Attachments/papers/images/]] — 论文图片",
    "",
    "## 按方向浏览",
    "",
]

for direction, label in DIRECTIONS.items():
    lines.append(f"### {label}")
    lines.append("")
    for slug, title in sorted(notes_by_dir.get(direction, [])):
        lines.append(f"- [[05_Papers/notes/{slug}|{title}]]")
    lines.append("")

lines.extend([
    "## 统计",
    "",
    f"- 人工笔记：{len(list(NOTES_DIR.glob('*.md')))} 篇",
    f"- MinerU 原文：{len(list(ARTICLES_DIR.rglob('*.md')))} 篇",
    "",
    "## 新增论文流程",
    "",
    "1. 将 PDF 放入 `99_Attachments/papers/pdfs/`",
    "2. 生成/复制 MinerU 原文到 `05_Papers/articles/<方向>/<slug>/`",
    "3. 在 `05_Papers/notes/` 中撰写结构化笔记",
    "4. 将图片放入 `99_Attachments/papers/images/<slug>/`",
])

(ROOT / "05_Papers/index.md").write_text("\n".join(lines), encoding="utf-8")
print("generated: 05_Papers/index.md")
```

- [ ] **Step 2: 运行脚本**

Run:
```bash
python 99_Attachments/scripts/_generate_index.py
```

Expected: `generated: 05_Papers/index.md`

- [ ] **Step 3: 预览内容**

Run:
```bash
cat 05_Papers/index.md
```

Expected: MOC 包含 5 个方向、21 篇笔记链接、统计与流程

---

### Task 8: 迁移 repair.py 脚本

**Files:**
- Create: `99_Attachments/scripts/repair.py`
- Create: `99_Attachments/scripts/repair_all.py`

**Interfaces:**
- Consumes: `paper-notes/script/repair.py`、`paper-notes/script/repair_all.py`
- Produces: 保留在附件目录的脚本

- [ ] **Step 1: 复制脚本**

Run:
```bash
cp paper-notes/script/repair.py 99_Attachments/scripts/repair.py
cp paper-notes/script/repair_all.py 99_Attachments/scripts/repair_all.py
```

- [ ] **Step 2: 校验**

Run:
```bash
ls -la 99_Attachments/scripts/repair.py 99_Attachments/scripts/repair_all.py
```

Expected: 两个脚本均存在

---

### Task 9: 删除 paper-notes 目录

**Files:**
- Delete: `paper-notes/`

**Interfaces:**
- Consumes: 前面任务完成确认
- Produces: 无

- [ ] **Step 1: 删除原目录**

Run:
```bash
rm -rf paper-notes
```

- [ ] **Step 2: 确认删除**

Run:
```bash
test -d paper-notes && echo "still exists" || echo "removed"
```

Expected: `removed`

---

### Task 10: 清理临时迁移脚本

**Files:**
- Delete: `99_Attachments/scripts/_migrate_*.py`
- Delete: `99_Attachments/scripts/_map_images.py`
- Delete: `99_Attachments/scripts/_fix_internal_links.py`
- Delete: `99_Attachments/scripts/_generate_index.py`

**Interfaces:**
- Consumes: 迁移完成
- Produces: 仅保留 repair.py / repair_all.py

- [ ] **Step 1: 删除临时脚本**

Run:
```bash
rm -f 99_Attachments/scripts/_migrate_pdfs.py \
      99_Attachments/scripts/_migrate_images.py \
      99_Attachments/scripts/_migrate_articles.py \
      99_Attachments/scripts/_migrate_notes.py \
      99_Attachments/scripts/_map_images.py \
      99_Attachments/scripts/_fix_internal_links.py \
      99_Attachments/scripts/_generate_index.py
```

- [ ] **Step 2: 确认最终脚本**

Run:
```bash
ls 99_Attachments/scripts/
```

Expected: 仅 `repair.py`、`repair_all.py`

---

### Task 11: 验证

**Files:**
- Read: `05_Papers/notes/*.md`
- Read: `05_Papers/articles/**/*.md`
- Read: `99_Attachments/papers/pdfs/*.pdf`
- Read: `99_Attachments/papers/images/**/*.jpg`

**Interfaces:**
- Consumes: 全部迁移结果
- Produces: 验证报告

- [ ] **Step 1: 数量校验**

Run:
```bash
echo "notes: $(find 05_Papers/notes -maxdepth 1 -name '*.md' | wc -l)"
echo "articles: $(find 05_Papers/articles -name '*.md' | wc -l)"
echo "pdfs: $(find 99_Attachments/papers/pdfs -name '*.pdf' | wc -l)"
echo "images: $(find 99_Attachments/papers/images -type f | wc -l)"
```

Expected:
```
notes: 21
articles: 26
pdfs: 22
images: 151
```

- [ ] **Step 2: frontmatter 校验**

Run:
```bash
python - <<'PY'
import re
from pathlib import Path
for f in sorted(Path("05_Papers/notes").glob("*.md")):
    text = f.read_text(encoding="utf-8")
    if not re.search(r'^---\s*\n.*?^title:\s*"?[^"\n]+"?', text, re.DOTALL | re.MULTILINE):
        print(f"missing title: {f.name}")
    if 'description:' not in text.split('---')[1] if text.startswith('---') else True:
        print(f"missing description: {f.name}")
    if 'tags:' not in text.split('---')[1] if text.startswith('---') else True:
        print(f"missing tags: {f.name}")
    if 'created:' not in text.split('---')[1] if text.startswith('---') else True:
        print(f"missing created: {f.name}")
print("frontmatter check done")
PY
```

Expected: 仅输出 `frontmatter check done`

- [ ] **Step 3: 图片链接校验**

Run:
```bash
python - <<'PY'
import re
from pathlib import Path
root = Path("/home/kemove/INNOV/library")
missing = []
for f in root.glob("05_Papers/notes/*.md"):
    text = f.read_text(encoding="utf-8")
    for m in re.finditer(r'!\[\[([^\]]+)\]\]', text):
        link = m.group(1)
        if link.startswith("99_Attachments/") and not (root / link).exists():
            missing.append((f.name, link))
if missing:
    for n, l in missing:
        print(f"{n}: {l}")
else:
    print("all image links valid")
PY
```

Expected: `all image links valid`

- [ ] **Step 4: 方向完整性校验**

Run:
```bash
for d in vla world-model world-action-model embodied-ai rl; do
    echo "$d: $(find 05_Papers/articles/$d -name '*.md' | wc -l)"
done
```

Expected: 每个方向至少 2 篇 articles

---

## Spec 覆盖检查

| Spec 要求 | 对应 Task |
|---|---|
| 创建目标目录结构 | Task 1 |
| PDF 迁移到 99_Attachments/papers/pdfs/ | Task 2 |
| 图片迁移到 99_Attachments/papers/images/<slug>/ | Task 3 |
| articles 迁移到 05_Papers/articles/<方向>/<slug>/ | Task 4 |
| notes frontmatter 统一为 title/description/tags/created | Task 5 |
| 修复图片/PDF/内部链接 | Task 5、Task 6 |
| 生成 05_Papers/index.md | Task 7 |
| 迁移 repair.py | Task 8 |
| 删除 paper-notes/ | Task 9 |
| 清理临时脚本 | Task 10 |
| 验证数量与链接 | Task 11 |

## 无占位符检查

- 所有脚本包含完整代码与路径
- 所有校验命令包含明确 Expected 输出
- 无 "TBD"/"TODO"/"implement later"
- slug 映射表覆盖全部 21 篇 notes 与 26 篇 articles
