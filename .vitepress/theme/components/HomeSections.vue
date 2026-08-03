<!-- 首页栏目：三个天蓝玻璃小卡入口 -->
<template>
  <div class="home-sections">
    <a v-for="card in cards" :key="card.title" class="section-card" :href="withBase(card.link)">
      <div class="section-card__icon">{{ card.icon }}</div>
      <h2 class="section-card__title">{{ card.title }}</h2>
      <p class="section-card__desc">{{ card.desc }}</p>
      <span class="section-card__more">共 {{ card.count }} 篇 →</span>
    </a>
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'
import { withBase } from 'vitepress'
import type { SectionData } from '../data/sections.data.ts'

// 数据由 theme/index.ts 从构建期 data loader provide 进来
const data = inject<SectionData>('sectionsData')!

const cards = computed(() => [
  {
    icon: '📄',
    title: '论文笔记',
    desc: 'VLA、世界模型、强化学习方向的精读与批注',
    link: '/05_Papers/',
    count: data.counts.papers,
  },
  {
    icon: '🛠',
    title: '我的项目',
    desc: 'VLA 训练与机器人部署的实战复盘',
    link: '/projects',
    count: data.counts.projects,
  },
  {
    icon: '🤖',
    title: 'AI 杂记',
    desc: '工具链与自动化工作流随手记',
    link: '/ai',
    count: data.counts.ai,
  },
])
</script>

<style scoped>
.home-sections {
  max-width: 1152px;
  margin: 0 auto;
  padding: 24px 24px 96px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

/* 天蓝玻璃小卡 */
.section-card {
  display: flex;
  flex-direction: column;
  padding: 28px;
  border-radius: 18px;
  background: var(--apple-glass-bg);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--apple-glass-border);
  box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s;
}
.section-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(14, 165, 233, 0.22);
}
.section-card__icon {
  font-size: 28px;
  margin-bottom: 12px;
}
.section-card__title {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.01em;
  border: none;
  padding: 0;
}
.section-card__desc {
  margin: 0 0 16px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--vp-c-text-2);
  flex: 1;
}
.section-card__more {
  font-size: 13px;
  font-weight: 500;
  color: var(--apple-accent);
}
</style>
