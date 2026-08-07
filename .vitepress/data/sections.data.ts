// 构建期加载内容区 frontmatter 与论文手动分组，供首页分区卡片展示
import fs from 'node:fs'
import path from 'node:path'
import { createContentLoader } from 'vitepress'

export interface SectionItem {
  title: string
  url: string
  created: string
  description: string
  tags: string[]
  // AI 之旅分区：skill=我的 Skills 卡片，article=Claude Code 专栏文章
  kind: string
}

export interface PaperGroup {
  id: string
  label: string
  icon: string
  items: SectionItem[]
}

export interface SectionData {
  papers: SectionItem[]
  paperGroups: PaperGroup[]
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
    tags: normalizeTags(page.frontmatter.tags),
    kind: String(page.frontmatter.kind ?? ''),
  }
}

function normalizeTags(raw: any): string[] {
  if (Array.isArray(raw)) return raw.map(String)
  if (typeof raw === 'string') return raw.split(',').map(s => s.trim()).filter(Boolean)
  return []
}

// 从 05_Papers/by-topic.md 解析手动分组，供 PapersIndex 按研究方向渲染卡片
function loadPaperGroups(papers: SectionItem[]): PaperGroup[] {
  const file = path.join(process.cwd(), '05_Papers/by-topic.md')
  if (!fs.existsSync(file)) return []

  const text = fs.readFileSync(file, 'utf-8')
  // 跳过 YAML frontmatter
  const body = text.replace(/^---\n[\s\S]*?\n---\n/, '')

  const sectionRe = /^##\s+(.+)$/gm
  const sections: { name: string; start: number }[] = []
  let m: RegExpExecArray | null
  while ((m = sectionRe.exec(body))) sections.push({ name: m[1].trim(), start: m.index })

  const result: PaperGroup[] = []
  for (let i = 0; i < sections.length; i++) {
    const name = sections[i].name
    // 全部论文列表与卡片视图重复，跳过
    if (name.startsWith('全部论文') || name.includes('字母序')) continue

    const end = i + 1 < sections.length ? sections[i + 1].start : body.length
    const sectionBody = body.slice(sections[i].start, end)

    const items: SectionItem[] = []
    const linkRe = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g
    let lm: RegExpExecArray | null
    while ((lm = linkRe.exec(sectionBody))) {
      const slug = lm[1].trim().split('/').pop()!
      const item = papers.find((p) => p.url.endsWith(`/${slug}`))
      if (item) items.push(item)
    }

    if (items.length) {
      result.push({
        id: name.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, ''),
        label: name,
        icon: '',
        items,
      })
    }
  }

  return result
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
      const paperGroups = loadPaperGroups(papers)
      // 只展示自己的项目，排除 MOC 页
      const own = byDir('/06_Projects/own').filter((p) => {
        const url = p.url.replace(/\/$/, '')
        return !url.endsWith('/innov-projects') && !url.endsWith('/own')
      })
      // 剔除 MOC 索引页与站内索引页（srcExclude 后 contentLoader 仍会扫到后者）
      const ai = byDir('/02_AI/skills').filter((p) => {
        const url = p.url.replace(/\/$/, '')
        return url !== '/02_AI/skills' && !url.endsWith('/Claude-Code-Skills')
      })
      return {
        papers,
        paperGroups,
        ownProjects: own,
        aiSkills: ai,
        counts: { papers: papers.length, projects: own.length, ai: ai.length },
      }
    },
  }
)
