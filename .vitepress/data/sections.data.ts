// 构建期加载三个内容区的 frontmatter，供首页分区卡片展示最新条目
import { createContentLoader } from 'vitepress'

export interface SectionItem {
  title: string
  url: string
  created: string
  description: string
}

export interface SectionData {
  papers: SectionItem[]
  ownProjects: SectionItem[]
  aiSkills: SectionItem[]
  counts: { papers: number; projects: number; ai: number }
}

declare const data: SectionData
export { data }

function toItem(page: { url: string; frontmatter: Record<string, any> }): SectionItem {
  // gray-matter 会把 created 解析成 Date，统一转成 YYYY-MM-DD 字符串
  const raw = page.frontmatter.created
  const created = raw instanceof Date ? raw.toISOString().slice(0, 10) : String(raw ?? '')
  return {
    title: page.frontmatter.title ?? page.url.split('/').pop() ?? '',
    url: page.url,
    created,
    description: page.frontmatter.description ?? '',
  }
}

export default createContentLoader(
  ['05_Papers/notes/*.md', '06_Projects/own/*.md', '02_AI/skills/*.md'],
  {
    transform(raw): SectionData {
      const byDir = (prefix: string) =>
        raw
          .filter((p) => p.url.startsWith(prefix))
          .map(toItem)
          .sort((a, b) => b.created.localeCompare(a.created))
      const papers = byDir('/05_Papers/notes')
      // 只展示自己的项目，排除 MOC 页
      const own = byDir('/06_Projects/own').filter((p) => !p.url.endsWith('/innov-projects') && !p.url.endsWith('/own/'))
      const ai = byDir('/02_AI/skills')
      return {
        papers,
        ownProjects: own,
        aiSkills: ai,
        counts: { papers: papers.length, projects: own.length, ai: ai.length },
      }
    },
  }
)
