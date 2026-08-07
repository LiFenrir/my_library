<!-- AI 技能名片：展开 frontmatter 摘要，不跳转 -->
<template>
  <div class="skill-card">
    <div class="skill-card__top">
      <span class="skill-card__icon">{{ icon }}</span>
      <span class="skill-card__date">{{ item.created }}</span>
    </div>
    <h3 class="skill-card__title">{{ item.title }}</h3>
    <p class="skill-card__desc">{{ item.description }}</p>
    <div class="skill-card__tags">
      <span v-for="t in item.tags" :key="t" class="skill-card__tag">{{ t }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SectionItem } from '../../data/sections.data'

const props = defineProps<{ item: SectionItem }>()

const icon = computed(() => {
  const t = props.item.title.toLowerCase()
  if (t.includes('mineru')) return '⛏️'
  if (t.includes('archive')) return '📥'
  return '🤖'
})
</script>

<style scoped>
.skill-card {
  display: flex;
  flex-direction: column;
  padding: 24px;
  border-radius: var(--apple-radius-l, 18px);
  background: rgba(255, 255, 255, 0.42);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--apple-glass-border);
  box-shadow: 0 4px 20px rgba(14, 165, 233, 0.06);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s;
}
.dark .skill-card {
  background: rgba(14, 165, 233, 0.08);
}
.skill-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 36px rgba(14, 165, 233, 0.14);
}

.skill-card__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.skill-card__icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-size: 20px;
  background: linear-gradient(140deg, rgba(125, 211, 252, 0.32), rgba(129, 140, 248, 0.22));
  border: 1px solid var(--apple-glass-border);
}
.skill-card__date {
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.skill-card__title {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: -0.01em;
  border: none;
  padding: 0;
}
.skill-card__desc {
  margin: 0 0 14px;
  font-size: 13px;
  line-height: 1.6;
  color: var(--vp-c-text-2);
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.skill-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.skill-card__tag {
  font-size: 11px;
  padding: 3px 9px;
  border-radius: 980px;
  background: color-mix(in srgb, var(--apple-accent) 10%, transparent);
  color: var(--apple-accent);
  white-space: nowrap;
}
</style>
