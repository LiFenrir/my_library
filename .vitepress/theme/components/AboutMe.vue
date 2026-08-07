<!-- 首页个人简介 -->
<template>
  <section class="about">
    <div class="about-hero">
      <div class="about-hero__avatar" aria-hidden="true">LF</div>
      <div class="about-hero__main">
        <h1 class="about-hero__name">Lifenrir个人主页</h1>

        <div class="about-hero__contacts">
          <a class="about-contact" href="https://github.com/LiFenrir" target="_blank" rel="noopener">
            <svg class="about-contact__icon" viewBox="0 0 24 24" aria-hidden="true">
              <path fill="currentColor" d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.28-.01-1.02-.01-2-3.2.69-3.89-1.54-3.89-1.54-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.76 2.7 1.25 3.36.96.1-.74.4-1.25.73-1.54-2.56-.29-5.25-1.28-5.25-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.18 1.18a11.1 11.1 0 0 1 5.82 0c2.2-1.49 3.17-1.18 3.17-1.18.64 1.59.24 2.77.12 3.06.74.81 1.19 1.84 1.19 3.1 0 4.43-2.7 5.41-5.27 5.69.42.36.79 1.08.79 2.18 0 1.57-.01 2.84-.01 3.23 0 .31.21.67.8.56C20.71 21.39 24 17.08 24 12c0-6.35-5.15-11.5-11.5-11.5z"/>
            </svg>
            <span class="about-contact__label">GitHub</span>
            <span class="about-contact__value">LiFenrir</span>
          </a>
          <a class="about-contact" href="mailto:jianbin3428@gmail.com">
            <svg class="about-contact__icon" viewBox="0 0 24 24" aria-hidden="true">
              <path fill="currentColor" d="M1.75 4.5h20.5c.42 0 .75.33.75.75v13.5c0 .42-.33.75-.75.75H1.75a.75.75 0 0 1-.75-.75V5.25c0-.42.33-.75.75-.75Zm.75 1.5v.7l9.5 5.94 9.5-5.94v-.7H2.5Zm0 2.45v9.05h19V8.45l-9.23 5.77a.75.75 0 0 1-.54.14.75.75 0 0 1-.54-.14L2.5 8.45Z"/>
            </svg>
            <span class="about-contact__label">邮箱</span>
            <span class="about-contact__value">jianbin3428@gmail.com</span>
          </a>
        </div>

        <p class="about-hero__role">
          具身智能从业者 · 关注 VLA、世界模型与机器人学习
        </p>

        <p class="about-hero__bio">
          这里是 LiFenrir 的个人站点，用来整理和展示日常沉淀的内容：
        </p>

        <ul class="about-hero__sections">
          <li>
            <strong>论文笔记</strong> —— VLA、世界模型、机器人学习等方向的精读与批注。
          </li>
          <li>
            <strong>我的项目</strong> —— VLA 训练、机器人部署与相关工程的实战复盘。
          </li>
          <li>
            <strong>AI 之旅</strong> —— 工具链、自动化工作流与 AI 使用经验的随手记。
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// 纯展示组件
</script>

<style scoped>
.about {
  max-width: 1080px;
  margin: 0 auto;
  padding: 72px 24px 8px;
}

.about-hero {
  display: flex;
  align-items: flex-start;
  gap: 28px;
}

.about-hero__avatar {
  flex-shrink: 0;
  width: 84px;
  height: 84px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, var(--apple-accent), #7dd3fc);
  box-shadow: 0 8px 24px rgba(14, 165, 233, 0.22);
}

.about-hero__main {
  flex: 1;
  min-width: 0;
}

.about-hero__name {
  margin: 0 0 14px;
  font-size: clamp(28px, 5vw, 42px);
  font-weight: 700;
  letter-spacing: -0.03em;
  border: none;
}

.about-hero__contacts {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.about-contact {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 980px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  color: var(--vp-c-text-2);
  background: rgba(255, 255, 255, 0.45);
  border: 1px solid rgba(14, 165, 233, 0.18);
  backdrop-filter: blur(12px);
  transition: color 0.2s, border-color 0.2s, background-color 0.2s;
}
.about-contact:hover {
  color: var(--apple-accent);
  border-color: rgba(14, 165, 233, 0.35);
  background: rgba(255, 255, 255, 0.65);
}
.dark .about-contact {
  background: rgba(14, 165, 233, 0.1);
  border-color: rgba(56, 189, 248, 0.18);
}
.dark .about-contact:hover {
  background: rgba(14, 165, 233, 0.18);
}

.about-contact__icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.about-contact__label {
  color: var(--apple-text-secondary);
  font-size: 13px;
}

.about-contact__value {
  color: var(--vp-c-text-1);
  font-weight: 600;
}

.about-hero__role {
  margin: 0 0 14px;
  font-size: 15px;
  font-weight: 500;
  color: var(--apple-accent);
}

.about-hero__bio {
  max-width: 760px;
  margin: 0 0 10px;
  font-size: 15px;
  line-height: 1.75;
  color: var(--vp-c-text-2);
}

.about-hero__sections {
  max-width: 760px;
  margin: 0;
  padding-left: 18px;
  font-size: 15px;
  line-height: 1.75;
  color: var(--vp-c-text-2);
}
.about-hero__sections li {
  margin-bottom: 6px;
}
.about-hero__sections strong {
  color: var(--vp-c-text-1);
  font-weight: 600;
}

@media (max-width: 640px) {
  .about {
    padding: 48px 16px 8px;
  }
  .about-hero {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 18px;
  }
  .about-hero__contacts {
    justify-content: center;
  }
  .about-hero__bio,
  .about-hero__sections {
    text-align: left;
  }
}
</style>
