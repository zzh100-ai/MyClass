<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const ready = ref(false)

onMounted(() => {
  setTimeout(() => (ready.value = true), 80)
})

const features = [
  { icon: '◆', title: '体系化课程', desc: '从入门到精通的完整学习路径' },
  { icon: '◇', title: '实战项目', desc: '边学边练，积累真实项目经验' },
  { icon: '○', title: '在线评测', desc: '即时反馈，精准定位薄弱环节' },
]
</script>

<template>
  <div class="home" :class="{ ready }">
    <!-- 装饰性几何背景 -->
    <div class="bg-geometry">
      <div class="geo-line geo-line-1"></div>
      <div class="geo-line geo-line-2"></div>
      <div class="geo-line geo-line-3"></div>
      <div class="geo-circle geo-circle-1"></div>
      <div class="geo-circle geo-circle-2"></div>
      <div class="geo-grid"></div>
    </div>

    <!-- 顶部导航 -->
    <NavBar />

    <!-- 主内容 -->
    <main class="main-content">
      <!-- 左侧英雄区域 -->
      <section class="hero">
        <div class="hero-tag">— 在线教育平台 —</div>
        <h1 class="hero-title">
          <span class="hero-word" style="--i: 1">让学习</span>
          <span class="hero-word" style="--i: 2">更有</span>
          <span class="hero-word hero-accent" style="--i: 3">深度</span>
        </h1>
        <p class="hero-desc">
          体系化的课程设计、真实的项目实战、精准的在线评测<br />
          重新定义你的学习方式
        </p>
        <button class="hero-cta">开始学习</button>
      </section>

      <!-- 右侧数据卡片 -->
      <section class="stats">
        <div class="stat-card" style="--d: 1">
          <div class="stat-number">12+</div>
          <div class="stat-label">课程方向</div>
          <div class="stat-border"></div>
        </div>
        <div class="stat-card" style="--d: 2">
          <div class="stat-number">200+</div>
          <div class="stat-label">精品课程</div>
          <div class="stat-border"></div>
        </div>
        <div class="stat-card" style="--d: 3">
          <div class="stat-number">50K+</div>
          <div class="stat-label">学习用户</div>
          <div class="stat-border"></div>
        </div>
      </section>
    </main>

    <!-- 底部特性卡片 -->
    <section class="features">
      <div
        v-for="(feat, idx) in features"
        :key="idx"
        class="feature-card"
        :style="'--d: ' + (idx + 4)"
      >
        <div class="feature-icon">{{ feat.icon }}</div>
        <h3 class="feature-title">{{ feat.title }}</h3>
        <p class="feature-desc">{{ feat.desc }}</p>
      </div>
    </section>

    <!-- 底部 -->
    <PageFooter />
  </div>
</template>

<style scoped>
/* ===== 页面样式 ===== */
.home {
  min-height: 100vh;
  background: linear-gradient(160deg, #1a1a3e 0%, #1e2a4a 30%, #1c2541 60%, #1a1a3e 100%);
  color: rgba(255, 255, 255, 0.94);
  font-family: 'Georgia', 'Noto Serif SC', 'SimSun', serif;
  overflow-x: hidden;
  position: relative;
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.home.ready {
  opacity: 1;
  transform: translateY(0);
}

/* ===== 装饰几何背景 ===== */
.bg-geometry {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.geo-line {
  position: absolute;
  background: linear-gradient(90deg, transparent, rgba(233, 69, 96, 0.12), transparent);
  height: 1px;
  transform: rotate(-8deg);
  animation: geoDrift 20s linear infinite;
}

.geo-line-1 {
  width: 140%;
  top: 30%;
  left: -20%;
  animation-delay: 0s;
}

.geo-line-2 {
  width: 120%;
  top: 55%;
  left: -10%;
  animation-delay: -7s;
  opacity: 0.5;
}

.geo-line-3 {
  width: 100%;
  top: 75%;
  left: 0%;
  animation-delay: -14s;
  opacity: 0.3;
}

@keyframes geoDrift {
  0% { transform: rotate(-8deg) translateX(0); }
  100% { transform: rotate(-8deg) translateX(-60px); }
}

.geo-circle {
  position: absolute;
  border: 1px solid rgba(233, 69, 96, 0.12);
  border-radius: 50%;
}

.geo-circle-1 {
  width: 600px;
  height: 600px;
  top: -200px;
  right: -150px;
}

.geo-circle-2 {
  width: 400px;
  height: 400px;
  bottom: -100px;
  left: -100px;
  border-color: rgba(212, 165, 116, 0.1);
}

.geo-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 80px 80px;
}

/* ===== 主内容区 ===== */
.main-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 60px 48px;
  max-width: 1200px;
  margin: 0 auto;
  gap: 80px;
}

/* ===== 英雄区域 ===== */
.hero {
  flex: 1;
  max-width: 580px;
}

.hero-tag {
  font-size: 0.75rem;
  letter-spacing: 4px;
  color: #d4a574;
  margin-bottom: 24px;
  opacity: 0;
  animation: fadeUp 0.6s 0.2s forwards;
}

.hero-title {
  font-size: 4.5rem;
  font-weight: 400;
  line-height: 1.15;
  margin: 0 0 28px;
  letter-spacing: 2px;
}

.hero-word {
  display: inline-block;
  opacity: 0;
  animation: fadeUp 0.6s forwards;
  animation-delay: calc(var(--i) * 0.15s + 0.3s);
}

.hero-accent {
  color: #e94560;
  position: relative;
}

.hero-accent::after {
  content: '';
  position: absolute;
  bottom: 4px;
  left: 0;
  width: 100%;
  height: 3px;
  background: #e94560;
  border-radius: 1px;
  transform: scaleX(0);
  transform-origin: left;
  animation: underlineReveal 0.6s 0.85s forwards;
}

@keyframes underlineReveal {
  to { transform: scaleX(1); }
}

.hero-desc {
  font-size: 1rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 36px;
  opacity: 0;
  animation: fadeUp 0.6s 0.8s forwards;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.hero-cta {
  background: transparent;
  border: 1px solid #e94560;
  color: #e94560;
  padding: 14px 40px;
  font-size: 0.95rem;
  letter-spacing: 3px;
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'Georgia', serif;
  opacity: 0;
  animation: fadeUp 0.6s 1s forwards;
  position: relative;
  overflow: hidden;
}

.hero-cta::before {
  content: '';
  position: absolute;
  inset: 0;
  background: #e94560;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
  z-index: -1;
}

.hero-cta:hover {
  color: #fff;
}

.hero-cta:hover::before {
  transform: scaleX(1);
  transform-origin: left;
}

/* ===== 数据卡片 ===== */
.stats {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex-shrink: 0;
}

.stat-card {
  position: relative;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 28px 32px;
  width: 180px;
  transition: all 0.3s;
  opacity: 0;
  animation: fadeUp 0.5s forwards;
  animation-delay: calc(var(--d) * 0.12s + 0.5s);
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(233, 69, 96, 0.3);
  transform: translateX(-4px);
}

.stat-number {
  font-size: 2.2rem;
  font-weight: 700;
  color: #e94560;
  margin-bottom: 6px;
  letter-spacing: 1px;
}

.stat-label {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: 1px;
}

.stat-border {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 0;
  height: 2px;
  background: #e94560;
  transition: width 0.4s ease;
}

.stat-card:hover .stat-border {
  width: 100%;
}

/* ===== 特性卡片 ===== */
.features {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
  gap: 40px;
  padding: 60px 48px;
  max-width: 1000px;
  margin: 0 auto;
}

.feature-card {
  flex: 1;
  max-width: 280px;
  text-align: center;
  padding: 36px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  opacity: 0;
  animation: fadeUp 0.5s forwards;
  animation-delay: calc(var(--d) * 0.1s + 0.6s);
  transition: border-color 0.3s;
}

.feature-card:hover {
  border-top-color: rgba(233, 69, 96, 0.35);
}

.feature-icon {
  font-size: 1.5rem;
  color: #e94560;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 1.05rem;
  font-weight: 400;
  margin: 0 0 10px;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.92);
}

.feature-desc {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.65);
  margin: 0;
  line-height: 1.6;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ===== 动画 ===== */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
