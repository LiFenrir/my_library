import mathjax3 from 'markdown-it-mathjax3'
import fs from 'node:fs'
import path from 'node:path'
import { defineConfig } from 'vitepress'
import { buildSidebar } from './theme/sidebar'
import { wikilinkPlugin } from './plugins/wikilink'

// 静态资源直接以 99_Attachments 为源：dev 由中间件提供，build 拷入 dist，无需 public 目录
const IMAGE_MIME: Record<string, string> = {
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.bmp': 'image/bmp',
}

function serveAttachments() {
  const src = path.join(process.cwd(), '99_Attachments')
  const distDest = path.join(process.cwd(), '.vitepress/dist/99_Attachments')

  // 只发布论文图片和站点图标，避免把 PDF 等大文件拷进产物
  const publishEntries = ['papers/images', 'moon.svg']

  function copyDir(from: string, to: string) {
    fs.mkdirSync(to, { recursive: true })
    for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
      const fromPath = path.join(from, entry.name)
      const toPath = path.join(to, entry.name)
      if (entry.isDirectory()) {
        copyDir(fromPath, toPath)
      } else {
        fs.copyFileSync(fromPath, toPath)
      }
    }
  }

  return {
    name: 'serve-attachments',
    // dev：拦截 /<base>/99_Attachments/* 请求，直接从源目录读文件
    configureServer(server: { middlewares: { use: (fn: (req: any, res: any, next: () => void) => void) => void } }) {
      server.middlewares.use((req, res, next) => {
        const url = decodeURIComponent((req.url ?? '').split('?')[0])
        const marker = '/99_Attachments/'
        const idx = url.indexOf(marker)
        if (idx === -1) return next()
        const file = path.join(src, url.slice(idx + marker.length))
        if (!file.startsWith(src) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
          res.statusCode = 404
          return res.end('not found')
        }
        res.setHeader('Content-Type', IMAGE_MIME[path.extname(file).toLowerCase()] ?? 'application/octet-stream')
        fs.createReadStream(file).pipe(res)
      })
    },
    // build：拷入 dist（client/server 两次构建会触发两次，幂等）
    closeBundle() {
      for (const entry of publishEntries) {
        const from = path.join(src, entry)
        if (!fs.existsSync(from)) continue
        const to = path.join(distDest, entry)
        if (fs.statSync(from).isDirectory()) copyDir(from, to)
        else {
          fs.mkdirSync(path.dirname(to), { recursive: true })
          fs.copyFileSync(from, to)
        }
      }
    },
  }
}

const mathCustomElements = [
  'math', 'maction', 'maligngroup', 'malignmark', 'menclose', 'merror', 'mfenced',
  'mfrac', 'mi', 'mlongdiv', 'mmultiscripts', 'mn', 'mo', 'mover', 'mpadded',
  'mphantom', 'mroot', 'mrow', 'ms', 'mscarries', 'mscarry', 'msgroup', 'mstack',
  'msline', 'mspace', 'msqrt', 'msrow', 'mstyle', 'msub', 'msup', 'msubsup',
  'mtable', 'mtd', 'mtext', 'mtr', 'munder', 'munderover', 'semantics',
  'mprescripts', 'none', 'annotation', 'annotation-xml',
]

export default defineConfig({
  title: 'Lifenrir个人主页',
  description: 'Lifenrir 的个人主页：具身智能从业者的论文笔记、项目复盘与 AI 之旅',
  lang: 'zh-CN',
  // GitHub Pages 项目页路径，按仓库名调整
  base: '/my_library/',
  cleanUrls: true,
  lastUpdated: true,

  head: [
    ['link', { rel: 'icon', href: '/my_library/99_Attachments/moon.svg' }],
    ['meta', { name: 'theme-color', content: '#38bdf8' }],
    ['meta', { property: 'og:title', content: 'Lifenrir个人主页' }],
    ['meta', { property: 'og:description', content: '具身智能从业者的论文笔记、项目复盘与 AI 之旅' }],
  ],

  // 只发布以下目录之外的内容一律排除（Inbox、附件、模板、工具链等）
  srcExclude: [
    '00_Inbox/**',
    '99_Attachments/**',
    '05_Papers/articles/**',
    '06_Projects/external/**', // 外部开源项目不在站点展示
    '02_AI/skills/Claude-Code-Skills.md', // 站内 skill 索引仅 Obsidian 内查阅
    'Templates/**',
    '07_Decisions/**',
    '08_Experiments/**',
    '09_Questions/**',
    '.venv/**',
    '.docs/**',
    '.obsidian/**',
    '.claude/**',
    'README.md',
    'CLAUDE.md',
  ],

  // 笔记间 Obsidian 链接较多，wikilink 插件已尽力转换，剩余死链不阻塞构建
  ignoreDeadLinks: true,

  markdown: {
    lineNumbers: true,
    theme: { light: 'github-light-default', dark: 'github-dark-default' },
    math: true,
    config: (md) => {
      md.use(mathjax3)
      md.use(wikilinkPlugin, '/my_library/')
    },
  },

  vue: {
    template: {
      // wikilink 图片直接引用 /99_Attachments 公开路径，关闭 img src 的模块导入转换
      transformAssetUrls: { img: [] },
      compilerOptions: {
        isCustomElement: (tag) => mathCustomElements.includes(tag),
      },
    },
  },

  // 开发服务器排除 .venv/ 等大目录，避免 inotify watch 数耗尽
  vite: {
    plugins: [serveAttachments()],
    server: {
      watch: {
        ignored: ['**/.git/**', '**/node_modules/**', '**/.venv/**'],
      },
    },
  },

  themeConfig: {
    // VPImage 会自动 withBase，这里不带 base 前缀
    logo: '/99_Attachments/moon.svg',
    siteTitle: 'Lifenrir个人主页',

    nav: [
      { text: '首页', link: '/' },
      { text: '论文笔记', link: '/05_Papers/by-topic' },
      { text: '我的项目', link: '/projects' },
      { text: 'AI 之旅', link: '/ai' },
    ],

    sidebar: buildSidebar(),

    // 内置 minisearch 全文搜索（构建期生成索引，无需外部服务）
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
          modal: {
            displayDetails: '显示详情',
            resetButtonTitle: '清除',
            backButtonTitle: '返回',
            noResultsText: '无结果',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },

    outline: { label: '本页目录', level: [2, 3] },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdatedText: '最近更新',
    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '回到顶部',
    socialLinks: [{ icon: 'github', link: 'https://github.com/LiFenrir' }],

    footer: {
      message: 'Powered by VitePress · 一片安静的数字花园',
      copyright: 'Copyright © 2025 LiFenrir',
    },
  },
})
