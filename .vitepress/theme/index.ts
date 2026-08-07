// 主题入口：扩展默认主题，注册全局组件与视口浮现动效
import DefaultTheme from 'vitepress/theme'
import { h, onMounted, watch, nextTick, defineComponent } from 'vue'
import { useRoute, useData } from 'vitepress'
import type { Theme } from 'vitepress'
import ScrollProgress from './components/ScrollProgress.vue'
import SkyBackdrop from './components/SkyBackdrop.vue'
import HomeSections from './components/HomeSections.vue'
import AboutMe from './components/AboutMe.vue'
import EntryCards from './components/EntryCards.vue'
import PapersIndex from './components/PapersIndex.vue'
import PaperCard from './components/PaperCard.vue'
import AiSkillCard from './components/AiSkillCard.vue'
import { data as sectionsData } from '../data/sections.data'
import './custom.css'

// 视口浮现：给正文与首页卡片加 .reveal，进入视口后切 .revealed
function useReveal() {
  const route = useRoute()
  let observer: IntersectionObserver | null = null

  const setup = () => {
    observer?.disconnect()
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    observer = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            e.target.classList.add('revealed')
            observer?.unobserve(e.target)
          }
        }
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.05 }
    )
    const targets = document.querySelectorAll(
      '.vp-doc h2, .vp-doc h3, .vp-doc p, .vp-doc li, .vp-doc div[class*="language-"], .ml-card'
    )
    targets.forEach((el) => {
      el.classList.add('reveal')
      observer!.observe(el)
    })
  }

  onMounted(() => nextTick(setup))
  watch(() => route.path, () => nextTick(setup))
}

export default {
  extends: DefaultTheme,
  Layout: defineComponent({
    setup() {
      const { page } = useData()
      // 仅「我的项目」「AI 之旅」详情页套玻璃拟态内容卡；论文笔记保持标准 wiki
      // 注意：用 relativePath（如 06_Projects/own/x.md）判断，route.path 会带 base 前缀
      return () =>
        h(
          'div',
          { class: { 'glass-doc': /^(02_AI|06_Projects)\//.test(page.value.relativePath) } },
          [
            h(DefaultTheme.Layout, null, {
              // 全站动态天空背景
              'layout-top': () => h(SkyBackdrop),
              // 导航栏内注入滚动进度条
              'nav-bar-content-before': () => h(ScrollProgress),
            }),
          ]
        )
    },
  }),
  enhanceApp({ app }) {
    app.component('SkyBackdrop', SkyBackdrop)
    app.component('HomeSections', HomeSections)
    app.component('AboutMe', AboutMe)
    app.component('EntryCards', EntryCards)
    app.component('PapersIndex', PapersIndex)
    app.component('PaperCard', PaperCard)
    app.component('AiSkillCard', AiSkillCard)
    // 首页分区卡片数据（构建期由 createContentLoader 生成）
    app.provide('sectionsData', sectionsData)
  },
  setup() {
    useReveal()
  },
} satisfies Theme
