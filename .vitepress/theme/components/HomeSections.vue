<!-- 首页栏目：论文笔记独占首行，项目与 AI 之旅并排下方 -->
<template>
  <div class="home-sections">
    <a class="ml-card ml-card-featured" :href="withBase('/05_Papers/by-topic')">
      <span class="ml-card-arrow">→</span>
      <div class="ml-card-icon">📄</div>
      <h2 class="ml-card-title">论文笔记</h2>
      <p class="ml-card-desc">VLA、世界模型、强化学习方向的精读与批注</p>
      <span class="ml-card-meta">共 {{ data.counts.papers }} 篇</span>
    </a>

    <div class="ml-cards ml-cards-secondary">
      <a class="ml-card" :href="withBase('/projects')">
        <span class="ml-card-arrow">→</span>
        <div class="ml-card-icon">🛠️</div>
        <h2 class="ml-card-title">我的项目</h2>
        <p class="ml-card-desc">VLA 训练与机器人部署的实战复盘</p>
        <span class="ml-card-meta">共 {{ data.counts.projects }} 项</span>
      </a>
      <a class="ml-card" :href="withBase('/ai')">
        <span class="ml-card-arrow">→</span>
        <div class="ml-card-icon">🤖</div>
        <h2 class="ml-card-title">AI 之旅</h2>
        <p class="ml-card-desc">工具链与自动化工作流随手记</p>
        <span class="ml-card-meta">共 {{ data.counts.ai }} 篇</span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { withBase } from 'vitepress'
import type { SectionData } from '../data/sections.data'

// 数据由 theme/index.ts 从构建期 data loader provide 进来
const data = inject<SectionData>('sectionsData')!
</script>

<style scoped>
.home-sections {
  max-width: 1080px;
  margin: 0 auto;
  padding: 24px 24px 96px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ml-card-featured {
  width: 100%;
  padding: 32px 28px;
}
.ml-card-featured .ml-card-icon {
  width: 54px;
  height: 54px;
  font-size: 26px;
}
.ml-card-featured .ml-card-title {
  font-size: 1.35rem;
}
.ml-card-featured .ml-card-desc {
  font-size: 0.95rem;
}

.ml-cards-secondary {
  max-width: 100%;
  margin: 0;
  padding: 0;
}

@media (max-width: 640px) {
  .home-sections {
    padding: 16px 16px 64px;
  }
}
</style>
