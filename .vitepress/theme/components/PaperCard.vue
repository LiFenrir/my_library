<!-- 论文笔记名片：标题、描述、标签、日期 -->
<template>
  <a class="paper-card" :href="withBase(item.url)">
    <h3 class="paper-card__title">{{ item.title }}</h3>
    <p class="paper-card__desc">{{ item.description }}</p>
    <div class="paper-card__meta">
      <span class="paper-card__date">{{ item.created }}</span>
      <span class="paper-card__tags">
        <span v-for="t in item.tags.slice(0, 3)" :key="t" class="paper-card__tag">{{ t }}</span>
      </span>
    </div>
  </a>
</template>

<script setup lang="ts">
import { withBase } from 'vitepress'
import type { SectionItem } from '../../data/sections.data'

defineProps<{ item: SectionItem }>()
</script>

<style scoped>
.paper-card {
  display: flex;
  flex-direction: column;
  padding: 24px;
  border-radius: var(--apple-radius-l, 18px);
  background: rgba(255, 255, 255, 0.42);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--apple-glass-border);
  box-shadow: 0 4px 20px rgba(14, 165, 233, 0.06);
  text-decoration: none;
  color: inherit;
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s;
}
.dark .paper-card {
  background: rgba(14, 165, 233, 0.08);
}
.paper-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 36px rgba(14, 165, 233, 0.14);
}

.paper-card__title {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: -0.01em;
  border: none;
  padding: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.paper-card__desc {
  margin: 0 0 14px;
  font-size: 13px;
  line-height: 1.6;
  color: var(--vp-c-text-2);
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.paper-card__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.paper-card__date {
  font-size: 12px;
  color: var(--vp-c-text-3);
  white-space: nowrap;
}
.paper-card__tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  justify-content: flex-end;
}
.paper-card__tag {
  font-size: 11px;
  padding: 1px 7px;
  border-radius: 980px;
  background: color-mix(in srgb, var(--apple-accent) 12%, transparent);
  color: var(--apple-accent);
  white-space: nowrap;
}
</style>
