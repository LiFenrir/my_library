---
title: "Resolution-robust Large Mask Inpainting with Fourier Convolutions"
description: "基于快速傅里叶卷积（FFC）的单阶段大掩码图像修复方法，具有全图感受野、高分辨率泛化能力和高参数效率。"
tags: ["图像修复", "Inpainting", "data-processing", "傅里叶卷积"]
created: 2026-07-28
---

# Resolution-robust Large Mask Inpainting with Fourier Convolutions

## 基本信息
- **作者**: Roman Suvorov, Elizaveta Logacheva, Anton Mashikhin, Anastasia Remizova, Arsenii Ashukha, Aleksei Silvestrov, Naejin Kong, Harshith Goka, Kiwoong Park, Victor Lempitsky
- **单位**: Samsung AI Center Moscow, Samsung Research, EPFL, Skolkovo Institute of Science and Technology
- **发表**: 2021
- **链接**: https://github.com/saic-mdal/lama
- **项目主页**: https://saic-mdal.github.io/lama-project/

![[99_Attachments/papers/images/lama/fb8ab6f48ece80901b7fe844f656104300bea32eb448fde4425cd0b145d96a99.jpg]]

## 研究背景与动机

图像修复（inpainting）的核心难点在于：既要理解图像的全局结构，又要生成逼真的局部细节。

1. **大掩码困境**: 当缺失区域很大时，传统卷积网络感受野增长慢，难以利用 distant context 进行合理补全
2. **高分辨率泛化差**: 现有方法通常在训练分辨率上表现好，但迁移到更高分辨率时容易出现明显伪影
3. **多阶段模型复杂**: 主流方法常采用 coarse-to-fine 两阶段或结构引导流程，参数量和推理成本较高

## 核心贡献

![[99_Attachments/papers/images/lama/bf914df1d234cf6e0801c0b90f4a8fde992abcb5501c6196416da9a8d31dffa4.jpg]]

### 1. 基于快速傅里叶卷积（FFC）的单阶段修复网络
- 将通道分为 local 分支（常规卷积）和 global 分支（Real FFT2d + 频域 1×1 卷积 + Inverse Real FFT2d）
- 早期层即具备 image-wide receptive field，显著优于 ResNet 缓慢增长的有效感受野
- FFC 带来更好的周期性结构（砖墙、窗户、栅栏）生成能力，且天然具有尺度等变性

### 2. 高感受野感知损失（HRF Perceptual Loss）
- 使用基于语义分割任务、带空洞卷积的高感受野网络作为感知损失 backbone
- 促使生成结果在全局结构和形状上与目标一致，避免像素级损失导致的模糊平均

### 3. 激进的训练掩码生成策略
- 训练时均匀采样 wide masks（随机宽度膨胀的多边形链）和 box masks（任意长宽比矩形）
- 强制网络充分利用模型和损失函数的高感受野，提升对宽窄两种掩码的泛化

## 方法架构

```
输入: mask + masked image (4 通道)
    ↓
3 个下采样块
    ↓
6-18 个 FFC 残差块
    ↓
3 个上采样块
    ↓
输出: 3 通道修复图像
```

### 损失函数
总损失为加权和：
$$
\mathcal{L}_{\text{final}} = \kappa L_{\text{Adv}} + \alpha \mathcal{L}_{\text{HRFPL}} + \beta \mathcal{L}_{\text{DiscPL}} + \gamma R_1
$$

- **$L_{\text{Adv}}$**: Patch-level 非饱和对抗损失，仅对覆盖 mask 区域的 patch 判别真假
- **$\mathcal{L}_{\text{HRFPL}}$**: 高感受野感知损失，使用分割 ResNet50 + 空洞卷积
- **$\mathcal{L}_{\text{DiscPL}}$**: 判别器特征匹配损失，稳定训练
- **$R_1$**: 判别器梯度惩罚

### 训练细节
- 优化器：Adam（生成器 lr=1e-3，判别器 lr=1e-4）
- 训练 1M iterations，batch size 30
- 在 256×256 裁剪图上训练，原图来自 512×512 Places 图片
- Big LaMa：18 个 FFC 残差块，51M 参数，batch 120，8×V100 训练约 240 小时

## 实验与结论

### 数据集与指标
- **数据集**: Places、CelebA-HQ
- **指标**: FID、LPIPS（更适配大掩码修复的多模态特性）
- **测试掩码**: narrow masks、wide masks、segmentation masks

### 与基线对比
- LaMa-Fourier（27M）在 Places 512×512 和 CelebA-HQ 256×256 上整体优于 CoModGAN（109M）、MADF（85M）等强基线
- 在 wide masks 上优势尤其明显，且参数量仅为竞争者的 1/3～1/4

### 消融实验
- **FFC vs Regular vs Dilated**: FFC 在 wide masks 上显著优于常规卷积；空洞卷积次之，但高分辨率泛化不如 FFC
- **HRF PL**: 使用带空洞卷积的分割 backbone 的感知损失优于分类 VGG 或普通感知损失
- **Wide mask training**: 对 LaMa 和 RegionWise 而言，用宽掩码训练可同时提升宽窄掩码表现

### 高分辨率泛化
- 仅在 256×256 训练，直接全卷积推理到 512×512 甚至 1536×1536
- FFC 模型在 1536×1536 仍保持语义一致和细节完整，而常规卷积模型已出现严重伪影

## 核心优势

1. **感受野即一切**: 从网络架构、损失函数到训练掩码，三位一体放大有效感受野
2. **单阶段高效率**: 无需 coarse-to-fine 或多阶段结构，参数和推理成本更低
3. **跨分辨率泛化**: FFC 的频域操作使模型对训练未见分辨率具有惊人鲁棒性
4. **周期性结构友好**: 特别适合建筑、栅栏、窗户等规则重复纹理

## 工程价值

- **可用场景**: 图像去水印、物体移除、Real2Sim 资产管线中的背景修复、数据增强
- **部署成本**: LaMa-Fourier 27M 参数，推理速度仅比同规模常规卷积慢约 20%，性价比高
- **开源情况**: 代码和预训练模型已开源，基于 PyTorch + PyTorch-Lightning + Hydra

## 局限与思考

- **透视畸变**: 在强透视变换的周期性结构上表现下降
- **非数据分布图像**: 对互联网上的复杂、非数据集图片仍可能失败
- **与生成式模型对比**: 作为判别式前馈网络，不如扩散模型灵活，但速度和可控性更优

> 我的理解：LaMa 的核心 insight 是「大掩码修复需要全局上下文」，并通过 FFC 在架构层面低成本实现全图感受野。这个方法至今仍是非常有工程价值的 baseline，尤其适合作为数据预处理或 Real2Sim 管线的一环。

## 相关论文
- [[05_Papers/articles/gs-playground|gs-playground]] — 在其 Real2Sim 管线中使用 LaMa 进行背景修复
- Fast Fourier Convolution (Chi et al., NeurIPS 2020) — FFC 算子原文
- DeepFill v2、EdgeConnect、CoModGAN、MADF — 同期图像修复方法

## 原文

[[05_Papers/articles/lama|lama]]
