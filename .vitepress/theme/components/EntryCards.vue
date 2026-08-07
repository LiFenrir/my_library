<!-- 条目卡片网格：项目 / AI 之旅列表页用，与首页同款天蓝玻璃小卡 -->
<template>
  <div class="entry-cards-page">
    <header class="entry-cards-page__header">
      <h1 class="entry-cards-page__title">{{ title }}</h1>
      <p class="entry-cards-page__subtitle">{{ subtitle }}</p>
    </header>
    <div class="entry-cards">
      <a v-for="item in items" :key="item.url" class="entry-card" :href="withBase(item.url)">
        <div class="entry-card__icon">{{ icon }}</div>
        <h2 class="entry-card__title">{{ item.title }}</h2>
        <p class="entry-card__desc">{{ item.description }}</p>
        <span class="entry-card__more">阅读 →</span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'
import { withBase } from 'vitepress'
import type { SectionData } from '../data/sections.data.ts'

// section: 展示哪个栏目的条目
const props = defineProps<{ section: 'projects' | 'ai' }>()

const data = inject<SectionData>('sectionsData')!
const items = computed(() => (props.section === 'projects' ? data.ownProjects : data.aiSkills))
const icon = computed(() => (props.section === 'projects' ? '🛠' : '🤖'))
const title = computed(() => (props.section === 'projects' ? '我的项目' : 'AI 之旅'))
const subtitle = computed(() =>
  props.section === 'projects' ? 'VLA 训练与机器人部署的实战复盘' : '工具链与自动化工作流随手记'
)
</script>

<style scoped>
.entry-cards-page {
  max-width: 1152px;
  margin: 0 auto;
  padding: 48px 24px 96px;
}
.entry-cards-page__header {
  margin-bottom: 32px;
}
.entry-cards-page__title {
  margin: 0 0 8px;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.entry-cards-page__subtitle {
  margin: 0;
  font-size: 15px;
  color: var(--vp-c-text-2);
}

.entry-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

/* 与首页一致的天蓝玻璃小卡 */
.entry-card {
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
.entry-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(14, 165, 233, 0.22);
}
.entry-card__icon {
  font-size: 28px;
  margin-bottom: 12px;
}
.entry-card__title {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.01em;
  border: none;
  padding: 0;
}
.entry-card__desc {
  margin: 0 0 16px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--vp-c-text-2);
  flex: 1;
}
.entry-card__more {
  font-size: 13px;
  font-weight: 500;
  color: var(--apple-accent);
}
</style>
