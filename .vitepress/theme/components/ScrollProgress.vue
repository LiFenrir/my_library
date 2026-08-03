<!-- 顶部滚动进度条：transform 驱动，不触发 layout -->
<template>
  <div class="scroll-progress" aria-hidden="true">
    <div class="scroll-progress__bar" :style="{ transform: `scaleX(${progress})` }"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const progress = ref(0)
let ticking = false

// rAF 节流 + passive 监听，滚动事件里只做一次 transform 写入
function onScroll() {
  if (ticking) return
  ticking = true
  requestAnimationFrame(() => {
    const el = document.documentElement
    const max = el.scrollHeight - el.clientHeight
    progress.value = max > 0 ? Math.min(el.scrollTop / max, 1) : 0
    ticking = false
  })
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  z-index: calc(var(--vp-z-index-nav) + 1);
  pointer-events: none;
}
.scroll-progress__bar {
  height: 100%;
  transform-origin: 0 50%;
  background: linear-gradient(90deg, var(--apple-accent), #818cf8);
  transition: transform 0.1s linear;
}
</style>
