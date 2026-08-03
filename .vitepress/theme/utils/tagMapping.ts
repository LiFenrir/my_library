// 共享分类逻辑：tag → 研究方向映射，sidebar 和 PapersIndex 共用
export interface TagGroup {
  id: string
  label: string
  icon: string
  tags: string[]
}

// 优先级从高到低：更具体的分类先匹配
export const TAG_GROUPS: TagGroup[] = [
  { id: 'world-action-models', label: '世界动作模型', icon: '🎬', tags: ['世界动作模型', 'WAM'] },
  { id: 'world-models',        label: '世界模型',     icon: '🌍', tags: ['世界模型', 'World Models', 'JEPA'] },
  { id: 'vla',                 label: 'VLA',          icon: '🤖', tags: ['VLA'] },
  { id: 'rl',                  label: 'Reinforcement Learning', icon: '🎮', tags: ['RL', 'Reinforcement Learning'] },
  { id: 'embodied-ai',         label: 'Embodied AI',  icon: '🦾', tags: ['具身智能', 'Embodied AI', 'Foundation Model', 'Cross-Embodiment'] },
  { id: 'data-processing',     label: 'Data Processing', icon: '📊', tags: ['data-processing', 'Data Processing', '分割', 'SAM'] },
]

export const CATCH_ALL = { id: 'other', label: '其他', icon: '📄' }

/** 首个匹配的 TAG_GROUPS tag 决定归属，无匹配返回 'other' */
export function classifyPaper(paperTags: string[]): string {
  for (const group of TAG_GROUPS) {
    if (paperTags.some(t => group.tags.includes(t))) return group.id
  }
  return CATCH_ALL.id
}

export function getGroupById(id: string): TagGroup | typeof CATCH_ALL | undefined {
  if (id === CATCH_ALL.id) return CATCH_ALL
  return TAG_GROUPS.find(g => g.id === id)
}
