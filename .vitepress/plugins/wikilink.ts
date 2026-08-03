// markdown-it 插件：将 Obsidian [[wikilink]] 转为站内链接，未命中渲染为灰色纯文本
import fs from 'node:fs'
import path from 'node:path'
import type MarkdownIt from 'markdown-it'

const ROOT = process.cwd()

// 参与路由解析的内容目录（与 config 的 srcExclude 互补）
const CONTENT_DIRS = ['02_AI', '03_Robotics', '04_Embodied-AI', '05_Papers/notes', '06_Projects/own']

// basename（不含扩展名）→ 站点路由；目录名 → 其 index 路由
function buildRouteMap(): Map<string, string> {
  const map = new Map<string, string>()
  for (const dir of CONTENT_DIRS) {
    const abs = path.join(ROOT, dir)
    if (!fs.existsSync(abs)) continue
    for (const entry of fs.readdirSync(abs, { recursive: true, withFileTypes: true })) {
      if (!entry.name.endsWith('.md')) continue
      const rel = path.join(dir, path.relative(abs, path.join(entry.parentPath, entry.name)))
      const route = '/' + rel.replace(/\.md$/, '').replace(/\/index$/, '')
      const basename = path.basename(entry.name, '.md')
      if (basename === 'index') {
        map.set(dir.split('/')[0], '/' + dir.split('/')[0]) // 如 [[05_Papers]] → /05_Papers
        continue
      }
      if (!map.has(basename)) map.set(basename, route)
    }
  }
  return map
}

export function wikilinkPlugin(md: MarkdownIt) {
  const routes = buildRouteMap()

  md.core.ruler.push('wikilink', (state) => {
    for (const token of state.tokens) {
      if (token.type !== 'inline' || !token.children) continue
      const newChildren: typeof token.children = []
      for (const child of token.children) {
        if (child.type !== 'text' || !child.content.includes('[[')) {
          newChildren.push(child)
          continue
        }
        // 拆分文本中的 [[target|label]] / [[target]]
        const re = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g
        let last = 0
        let m: RegExpExecArray | null
        while ((m = re.exec(child.content))) {
          if (m.index > last) {
            const t = new state.Token('text', '', 0)
            t.content = child.content.slice(last, m.index)
            newChildren.push(t)
          }
          const target = m[1].trim()
          const label = (m[2] ?? m[1]).trim()
          const basename = target.split('/').pop()!.replace(/\/$/, '') || target
          const route = routes.get(basename) ?? routes.get(target.replace(/\/$/, ''))
          const html = new state.Token('html_inline', '', 0)
          html.content = route
            ? `<a href="${md.utils.escapeHtml(route)}" class="wikilink">${md.utils.escapeHtml(label)}</a>`
            : `<span class="wikilink-missing">${md.utils.escapeHtml(label)}</span>`
          newChildren.push(html)
          last = m.index + m[0].length
        }
        if (last < child.content.length) {
          const t = new state.Token('text', '', 0)
          t.content = child.content.slice(last)
          newChildren.push(t)
        }
      }
      token.children = newChildren
    }
  })
}
