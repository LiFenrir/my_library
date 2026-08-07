<!-- 分区首页：论文笔记 / AI 之旅的卡片网格 -->
<template>
  <div class="papers-index">
    <header class="papers-index__header">
      <h1 class="papers-index__title">{{ title }}</h1>
      <p class="papers-index__subtitle">{{ subtitle }}</p>
    </header>

    <section v-for="s in sections" :key="s.id" class="papers-group">
      <h2 v-if="s.label" class="papers-group__heading">
        <span v-if="s.icon" class="papers-group__icon">{{ s.icon }}</span>
        {{ s.label }}
        <span class="papers-group__count">{{ s.items.length }}</span>
      </h2>
      <div class="papers-grid">
        <component
          :is="cardComponent"
          v-for="item in s.items"
          :key="item.url"
          :item="item"
        />
      </div>
    </section>

    <p v-if="sections.length === 0" class="papers-index__empty">暂无笔记</p>
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'
import type { SectionData, SectionItem } from '../../data/sections.data'
import { TAG_GROUPS, CATCH_ALL, classifyPaper } from '../utils/tagMapping'
import PaperCard from './PaperCard.vue'

const props = withDefaults(defineProps<{ section?: 'papers' | 'ai' }>(), { section: 'papers' })

const data = inject<SectionData>('sectionsData')!

const isPapers = computed(() => props.section === 'papers')
// AI 之旅与论文笔记统一使用 PaperCard（自带链接跳转）
const cardComponent = computed(() => PaperCard)

const title = computed(() => (isPapers.value ? '论文笔记' : 'AI 之旅'))
const subtitle = computed(() =>
  isPapers.value
    ? `共 ${data.papers.length} 篇精读笔记，按研究方向分组`
    : `共 ${aiItems.value.length} 篇工具链与工作流记录`
)

// 数据层已剔除 index 与站内索引页
const aiItems = computed<SectionItem[]>(() => data.aiSkills)

const sourceItems = computed<SectionItem[]>(() => (isPapers.value ? data.papers : aiItems.value))

const sections = computed(() => {
  const items = sourceItems.value
  if (!isPapers.value) {
    // AI 之旅分两个专区：我的 Skills（kind=skill）与 Claude Code 专栏（kind=article 或未标注）
    const skills = items.filter((p) => p.kind === 'skill')
    const articles = items.filter((p) => p.kind !== 'skill')
    const zones = []
    if (skills.length) zones.push({ id: 'skills', label: '我的 Skills', icon: '🛠️', items: skills })
    if (articles.length) zones.push({ id: 'claude-code', label: 'Claude Code 专栏', icon: '🤖', items: articles })
    return zones
  }

  // 优先使用手动分组文件
  if (data.paperGroups?.length) {
    return data.paperGroups
  }

  // 无手动分组时回退到 tag 自动分类
  const grouped = new Map<string, SectionItem[]>()
  for (const p of items) {
    const gid = classifyPaper(p.tags)
    if (!grouped.has(gid)) grouped.set(gid, [])
    grouped.get(gid)!.push(p)
  }

  const result: { id: string; label: string; icon: string; items: SectionItem[] }[] = []
  for (const tg of TAG_GROUPS) {
    const gItems = grouped.get(tg.id)
    if (gItems?.length) {
      gItems.sort((a, b) => b.created.localeCompare(a.created))
      result.push({ id: tg.id, label: tg.label, icon: tg.icon, items: gItems })
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
  max-width: 100%;
  margin: 0 auto;
  padding: 32px clamp(16px, 4vw, 48px) 64px;
}

.papers-index__header {
  margin-bottom: 40px;
}
.papers-index__title {
  margin: 0 0 8px;
  font-size: clamp(24px, 4vw, 32px);
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
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
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
