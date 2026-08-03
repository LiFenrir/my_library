---
title: "Fast Fourier Convolution"
description: "利用频域卷积实现全图感受野的神经网络算子"
tags: [concept, ml, computer-vision, convolution, fourier]
created: 2026-08-03
---

# Fast Fourier Convolution (FFC)

FFC 将标准卷积扩展为双分支结构：local 分支（常规空间卷积）+ global 分支（频域卷积），使网络早期层即具备 image-wide receptive field。

## 原理

```
输入通道 → 分割为 local 分支 + global 分支
  local:  常规 Conv2d → 局部特征
  global: Real FFT2d → 频域 1×1 Conv → Inverse Real FFT2d → 全局特征
  → Concat → 融合输出
```

**频域 1×1 卷积**: 在傅里叶域中，1×1 卷积等价于空间域的全图卷积——每个频率分量与所有空间位置交互，天然具备全局感受野。

## 优势

- **早期全局感受野**: 不同于 ResNet 需要层层堆叠才能扩大感受野，FFC 第一层即可看到整图
- **周期性结构友好**: 频域操作天然感知周期性模式（砖墙、栅栏、窗户）
- **尺度等变性**: 频域表示的相对位置编码具有内在尺度不变性
- **高分辨率泛化**: 在 256×256 训练，可直接推理到 1536×1536 无伪影

## 应用

- 图像修复（LaMa）：大掩码需要全图上下文理解
- 图像生成：周期性纹理生成
- 任何需要长距离空间依赖的视觉任务

## 来源

- [[05_Papers/notes/lama|LaMa]] — 基于 FFC 的单阶段大掩码修复
- Fast Fourier Convolution (Chi et al., NeurIPS 2020) — FFC 算子原文
