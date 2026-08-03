import { defineConfig } from 'vitepress'
import { buildSidebar } from './theme/sidebar'
import { wikilinkPlugin } from './plugins/wikilink'

export default defineConfig({
  title: 'LiFenrir个人小站',
  description: 'LiFenrir 的个人主页：具身智能从业者的论文笔记、项目复盘与 AI 杂记',
  lang: 'zh-CN',
  // GitHub Pages 项目页路径，按仓库名调整
  base: '/library/',
  cleanUrls: true,

  // 只发布以下目录之外的内容一律排除（Inbox、附件、模板、工具链等）
  srcExclude: [
    '00_Inbox/**',
    '99_Attachments/**',
    '05_Papers/articles/**',
    '06_Projects/external/**', // 外部开源项目不在站点展示
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
    theme: { light: 'github-light-default', dark: 'github-dark-default' },
    config: (md) => md.use(wikilinkPlugin),
  },

  // 开发服务器排除 .venv/ 等大目录，避免 inotify watch 数耗尽
  vite: {
    server: {
      watch: {
        ignored: ['**/.git/**', '**/node_modules/**', '**/.venv/**'],
      },
    },
  },

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '论文笔记', link: '/05_Papers/' },
      { text: '我的项目', link: '/projects' },
      { text: 'AI 杂记', link: '/ai' },
      { text: '关于我', link: '/about' },
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
    socialLinks: [{ icon: 'github', link: 'https://github.com/LiFenrir' }],
  },
})
