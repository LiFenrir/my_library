<!-- 论文笔记首页：按研究方向分组的卡片网格 -->
<template>
  <div class="papers-index">
    <header class="papers-index__header">
      <h1 class="papers-index__title">论文笔记</h1>
      <p class="papers-index__subtitle">共 {{ totalCount }} 篇精读笔记，按研究方向分组</p>
    </header>

    <section v-for="section in sections" :key="section.id" class="papers-group">
      <h2 class="papers-group__heading">
        <span class="papers-group__icon">{{ section.icon }}</span>
        {{ section.label }}
        <span class="papers-group__count">{{ section.items.length }}</span>
      </h2>
      <div class="papers-grid">
        <a v-for="item in section.items" :key="item.url"
           class="paper-card"
           :href="withBase(item.url)">
          <h3 class="paper-card__title">{{ item.title }}</h3>
          <p class="paper-card__desc">{{ item.description }}</p>
          <div class="paper-card__meta">
            <span class="paper-card__date">{{ item.created }}</span>
            <span class="paper-card__tags">
              <span v-for="t in item.tags.slice(0, 3)" :key="t" class="paper-card__tag">{{ t }}</span>
            </span>
          </div>
        </a>
      </div>
    </section>

    <p v-if="sections.length === 0" class="papers-index__empty">暂无笔记</p>
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'
import { withBase } from 'vitepress'
import type { SectionData } from '../../data/sections.data'
import { TAG_GROUPS, CATCH_ALL, classifyPaper, getGroupById } from '../utils/tagMapping'

const data = inject<SectionData>('sectionsData')!

const totalCount = computed(() => data.papers.length)

const sections = computed(() => {
  const grouped = new Map<string, typeof data.papers>()
  for (const p of data.papers) {
    const gid = classifyPaper(p.tags)
    if (!grouped.has(gid)) grouped.set(gid, [])
    grouped.get(gid)!.push(p)
  }

  const result: { id: string; label: string; icon: string; items: typeof data.papers }[] = []
  for (const tg of TAG_GROUPS) {
    const items = grouped.get(tg.id)
    if (items?.length) {
      items.sort((a, b) => b.created.localeCompare(a.created))
      result.push({ id: tg.id, label: tg.label, icon: tg.icon, items })
    }
  }
  const other = grouped.get(CATCH_ALL.id)
  if (other?.length) {
    result.push({ id: CATCH_ALL.id, label: CATCH_ALL.label, icon: CATCH_ALL.icon, items: other })
  }
  return result
})
</script>

<style scoped>
.papers-index {
  max-width: 1152px;
  margin: 0 auto;
  padding: 48px 24px 96px;
}

.papers-index__header {
  margin-bottom: 40px;
}
.papers-index__title {
  margin: 0 0 8px;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.papers-index__subtitle {
  margin: 0;
  font-size: 15px;
  color: var(--vp-c-text-2);
}

.papers-group {
  margin-bottom: 48px;
}
.papers-group__heading {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.01em;
  border: none;
  padding: 0;
}
.papers-group__icon {
  font-size: 24px;
}
.papers-group__count {
  font-size: 13px;
  font-weight: 500;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg-alt);
  padding: 2px 10px;
  border-radius: 980px;
}

.papers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.paper-card {
  display: flex;
  flex-direction: column;
  padding: 24px;
  border-radius: var(--apple-radius-l, 18px);
  background: var(--apple-glass-bg);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--apple-glass-border);
  box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s;
}
.paper-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(14, 165, 233, 0.22);
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

.papers-index__empty {
  text-align: center;
  color: var(--vp-c-text-2);
  font-size: 15px;
  padding: 48px 0;
}

@media (max-width: 768px) {
  .papers-index {
    padding: 32px 16px 64px;
  }
  .papers-grid {
    grid-template-columns: 1fr;
  }
}
</style>
