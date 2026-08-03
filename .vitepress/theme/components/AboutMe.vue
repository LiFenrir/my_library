<!-- 关于我：双语个人信息 + 联系方式 + 栏目导览，全玻璃拟态卡片 -->
<template>
  <div class="about">
    <!-- 个人简介卡 -->
    <section class="about-hero glass">
      <div class="about-hero__avatar" aria-hidden="true">LF</div>
      <h1 class="about-hero__name">LiFenrir</h1>
      <p class="about-hero__role">
        具身智能从业者 · 终身学习者<br />
        <span class="en">Embodied AI Practitioner · Lifelong Learner</span>
      </p>
      <p class="about-hero__bio">
        你好，我是 LiFenrir，一名具身智能（Embodied AI）从业者，主要关注 VLA
        模型、世界模型与机器人学习，仍在不断学习 ing。这个站点是我的第二大脑，用来沉淀论文精读、
        项目复盘与技术杂记，记录从理论到落地的每一步。
      </p>
      <p class="about-hero__bio en">
        Hi, I'm LiFenrir, an Embodied AI practitioner focusing on VLA models, world
        models, and robot learning — still learning every day. This site is my second
        brain, where I distill paper notes, project retrospectives, and tech memos.
      </p>
      <div class="about-hero__contacts">
        <a class="contact-chip" href="https://github.com/LiFenrir" target="_blank" rel="noopener">
          <span class="contact-chip__icon">⌥</span> GitHub · LiFenrir
        </a>
        <a class="contact-chip" href="mailto:jianbin3428@gmail.com">
          <span class="contact-chip__icon">✉</span> jianbin3428@gmail.com
        </a>
      </div>
    </section>

    <!-- 栏目导览 -->
    <h2 class="about-section-title">站内栏目 <span class="en">/ What's inside</span></h2>
    <div class="about-grid">
      <a v-for="col in columns" :key="col.title" class="glass column-card" :href="withBase(col.link)">
        <div class="column-card__icon">{{ col.icon }}</div>
        <h3 class="column-card__title">{{ col.title }}</h3>
        <p class="column-card__desc">{{ col.desc }}</p>
        <p class="column-card__desc en">{{ col.descEn }}</p>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { withBase } from 'vitepress'

const columns = [
  {
    icon: '📄',
    title: '论文笔记',
    desc: 'VLA、世界模型、强化学习方向的精读与批注，按标准 Wiki 方式组织',
    descEn: 'Paper notes on VLA, world models, and RL — classic wiki style.',
    link: '/05_Papers/',
  },
  {
    icon: '🛠',
    title: '我的项目',
    desc: 'VLA 训练、在线 RL、机器人部署等实战项目的经验复盘',
    descEn: 'Retrospectives on VLA training, online RL, and robot deployment.',
    link: '/projects',
  },
  {
    icon: '🤖',
    title: 'AI 杂记',
    desc: '工具链、自动化工作流，以及学习过程中的随手记录',
    descEn: 'Tooling, automation workflows, and memos along the way.',
    link: '/ai',
  },
]
</script>

<style scoped>
.about {
  max-width: 880px;
  margin: 0 auto;
  padding: 48px 24px 96px;
}

/* 玻璃拟态通用卡：半透明 + 背景模糊 + 圆角矩形 */
.glass {
  background: var(--apple-glass-bg);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--apple-glass-border);
  border-radius: var(--apple-radius-l);
  box-shadow: 0 8px 32px rgba(14, 165, 233, 0.08);
}

.about-hero {
  padding: 48px 40px;
  text-align: center;
}
.about-hero__avatar {
  width: 88px;
  height: 88px;
  margin: 0 auto 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, var(--apple-accent), #5e5ce6);
  box-shadow: 0 8px 24px rgba(14, 165, 233, 0.35);
}
.about-hero__name {
  margin: 0 0 8px;
  font-size: 34px;
  font-weight: 700;
  letter-spacing: -0.02em;
  border: none;
}
.about-hero__role {
  margin: 0 0 24px;
  font-size: 15px;
  font-weight: 500;
  color: var(--apple-accent);
}
.about-hero__bio {
  max-width: 620px;
  margin: 0 auto 14px;
  font-size: 15px;
  line-height: 1.8;
  color: var(--vp-c-text-1);
}
.en {
  color: var(--apple-text-secondary);
  font-size: 0.92em;
}
.about-hero__contacts {
  margin-top: 28px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
}
.contact-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 980px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  color: var(--vp-c-text-1);
  background: var(--apple-glass-bg);
  border: 1px solid var(--apple-glass-border);
  transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.25s, color 0.25s;
}
.contact-chip:hover {
  transform: translateY(-2px);
  color: var(--apple-accent);
  border-color: var(--apple-accent);
}
.contact-chip__icon {
  color: var(--apple-accent);
}

.about-section-title {
  margin: 56px 0 20px;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.01em;
  border: none;
  text-align: center;
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}
.column-card {
  display: block;
  padding: 28px 24px;
  text-decoration: none;
  color: inherit;
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s;
}
.column-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(14, 165, 233, 0.18);
}
.column-card__icon {
  font-size: 26px;
  margin-bottom: 10px;
}
.column-card__title {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 600;
  border: none;
  padding: 0;
}
.column-card__desc {
  margin: 0 0 6px;
  font-size: 13.5px;
  line-height: 1.65;
  color: var(--vp-c-text-2);
}
</style>
