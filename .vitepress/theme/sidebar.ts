// 构建期扫描目录 frontmatter，自动生成 VitePress 侧边栏
import fs from 'node:fs'
import path from 'node:path'

const ROOT = process.cwd()

export interface SidebarEntry {
  text: string
  link: string
}

export interface SidebarGroup {
  text: string
  link?: string
  collapsed?: boolean
  items: (SidebarGroup | SidebarEntry)[]
}

// 读取 md 文件 frontmatter 的 title（无依赖简易解析）
function readTitle(file: string): string {
  try {
    const head = fs.readFileSync(file, 'utf-8').slice(0, 2000)
    const m = head.match(/^---\n([\s\S]*?)\n---/)
    const t = m?.[1].match(/^title:\s*["']?(.+?)["']?\s*$/m)
    return t?.[1] ?? path.basename(file, '.md')
  } catch {
    return path.basename(file, '.md')
  }
}

// 读取 frontmatter 的 created 日期，用于排序
function readCreated(file: string): string {
  try {
    const head = fs.readFileSync(file, 'utf-8').slice(0, 2000)
    const m = head.match(/^created:\s*(.+?)\s*$/m)
    return m?.[1] ?? ''
  } catch {
    return ''
  }
}

// 扫描目录下所有 md，按 created 倒序生成条目
function scanDir(dir: string, routeBase: string): SidebarEntry[] {
  const abs = path.join(ROOT, dir)
  if (!fs.existsSync(abs)) return []
  return fs
    .readdirSync(abs)
    .filter((f) => f.endsWith('.md') && f !== 'index.md')
    .sort((a, b) => readCreated(path.join(abs, b)).localeCompare(readCreated(path.join(abs, a))))
    .map((f) => {
      const slug = f.replace(/\.md$/, '')
      return { text: readTitle(path.join(abs, f)), link: `${routeBase}/${slug}` }
    })
}

// 论文笔记：解析 05_Papers/by-topic.md 的 `### 方向` 分组与 [[slug]] 链接
function papersGroups(): SidebarGroup[] {
  const indexFile = path.join(ROOT, '05_Papers/by-topic.md')
  const groups: SidebarGroup[] = []
  try {
    const content = fs.readFileSync(indexFile, 'utf-8')
    const sectionRe = /^###\s+(.+)$/gm
    const sections: { name: string; start: number }[] = []
    let m: RegExpExecArray | null
    while ((m = sectionRe.exec(content))) sections.push({ name: m[1].trim(), start: m.index })

    for (let i = 0; i < sections.length; i++) {
      const end = i + 1 < sections.length ? sections[i + 1].start : content.length
      const body = content.slice(sections[i].start, end)
      const items: SidebarEntry[] = []
      const linkRe = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g
      let lm: RegExpExecArray | null
      while ((lm = linkRe.exec(body))) {
        const slug = lm[1].trim().split('/').pop()!
        const noteFile = path.join(ROOT, '05_Papers/notes', `${slug}.md`)
        if (fs.existsSync(noteFile)) {
          items.push({ text: readTitle(noteFile), link: `/05_Papers/notes/${slug}` })
        }
      }
      if (items.length) groups.push({ text: sections[i].name, collapsed: true, items })
    }
  } catch {
    // index.md 缺失或格式变化时降级为平铺
  }
  return groups.length ? groups : [{ text: '全部笔记', items: scanDir('05_Papers/notes', '/05_Papers/notes') }]
}

export function buildSidebar() {
  // 仅论文笔记保留左侧目录树；我的项目 / AI 之旅为卡片列表页，无侧边栏
  return {
    '/05_Papers/': [
      { text: '论文专区', items: [] },
      ...papersGroups(),
    ] as SidebarGroup[],
  }
}
