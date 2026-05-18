<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCourseStore } from '@/stores/courses'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const route = useRoute()
const router = useRouter()
const courseStore = useCourseStore()
const authStore = useAuthStore()
const cartStore = useCartStore()

const course = computed(() => courseStore.currentCourse)

async function addToCart() {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  try {
    await cartStore.addCourse(course.value.id)
    alert('已添加到购物车')
  } catch (e) {
    alert(e.message || '添加失败')
  }
}

onMounted(() => {
  const id = route.params.id
  if (id) {
    courseStore.fetchCourse(id)
  }
})

/** 格式化时长：秒 → 分钟 */
function formatDuration(seconds) {
  if (!seconds) return ''
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return s ? `${m}:${String(s).padStart(2, '0')}` : `${m}分钟`
}

/** 统计总课时和总时长 */
const courseStats = computed(() => {
  if (!course.value?.chapters) return { lessons: 0, duration: 0 }
  let lessons = 0
  let duration = 0
  for (const ch of course.value.chapters) {
    if (ch.lessons) {
      lessons += ch.lessons.length
      for (const les of ch.lessons) {
        duration += les.duration || 0
      }
    }
  }
  return { lessons, duration }
})
</script>

<template>
  <div class="course-detail-page">
    <NavBar />

    <!-- 加载中 -->
    <div v-if="courseStore.detailLoading" class="state-msg">加载中...</div>

    <!-- 课程不存在 -->
    <div v-else-if="!course" class="state-msg">
      <p>课程不存在或已被删除</p>
      <button class="back-btn" @click="router.push('/courses')">返回课程列表</button>
    </div>

    <!-- 课程详情 -->
    <template v-else>
      <!-- TODO: 课程头部信息展示
             实现：
             1. 显示封面图（或首字母占位）
             2. 显示价格/免费标签
             3. 显示课程统计（课时数、总时长）
      -->
      <section class="hero-section">
        <div class="hero-bg">
          <img v-if="course.cover_image" :src="course.cover_image" />
          <div v-else class="hero-placeholder">{{ course.title?.[0] }}</div>
        </div>
        <div class="hero-overlay">
          <div class="hero-content">
            <h1 class="hero-title">{{ course.title }}</h1>
            <p v-if="course.subtitle" class="hero-subtitle">{{ course.subtitle }}</p>
            <div class="hero-meta">
              <span class="meta-teacher">讲师：{{ course.teacher_name }}</span>
              <span class="meta-lessons">{{ courseStats.lessons }} 课时</span>
              <span v-if="courseStats.duration" class="meta-duration">
                总时长 {{ formatDuration(courseStats.duration) }}
              </span>
              <span class="meta-students">{{ course.learn_count }} 人学习</span>
            </div>
            <div class="hero-price">
              <span v-if="course.is_free" class="price free">免费</span>
              <span v-else>
                <span class="price">¥{{ course.price }}</span>
                <span v-if="course.original_price" class="original">¥{{ course.original_price }}</span>
              </span>
              <button class="buy-btn">
                {{ course.is_free ? '立即学习' : '立即购买' }}
              </button>
              <button class="cart-add-btn" @click="addToCart">加入购物车</button>
            </div>
          </div>
        </div>
      </section>

      <main class="main-content">
        <div class="content-left">
          <!-- 课程简介 -->
          <section class="section">
            <h2 class="section-title">课程简介</h2>
            <div class="description" v-html="course.description"></div>
          </section>

          <!-- 章节列表 -->

          <!-- TODO: 章节和课时列表
                 实现：
                 1. 遍历 chapters，显示每个章节标题
                 2. 章节内遍历 lessons 显示课时
                 3. 可预览的课时（is_preview）显示"试看"标签
                 4. 显示课时时长
                 5. 点击课时需要学习权限（后续实现）
          -->
          <section class="section">
            <h2 class="section-title">课程目录</h2>
            <div class="chapter-list">
              <div v-for="chapter in course.chapters" :key="chapter.id" class="chapter-item">
                <div class="chapter-header">
                  <span class="chapter-title">{{ chapter.title }}</span>
                  <span class="chapter-meta">{{ chapter.lessons?.length || 0 }} 课时</span>
                </div>
                <div class="lesson-list">
                  <div
                    v-for="(lesson, idx) in chapter.lessons"
                    :key="lesson.id"
                    class="lesson-item"
                  >
                    <span class="lesson-index">{{ idx + 1 }}</span>
                    <span class="lesson-title">{{ lesson.title }}</span>
                    <span v-if="lesson.is_preview" class="lesson-preview">试看</span>
                    <span class="lesson-duration">
                      {{ formatDuration(lesson.duration) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- 右侧信息栏（预留） -->
        <aside class="content-sidebar">
          <div class="info-card">
            <h3>课程信息</h3>
            <div class="info-row">
              <span class="info-label">分类</span>
              <span class="info-value">{{ course.category_name }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">课时</span>
              <span class="info-value">{{ courseStats.lessons }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">状态</span>
              <span class="info-value">{{ course.status === 'published' ? '已发布' : '草稿' }}</span>
            </div>
          </div>
        </aside>
      </main>
    </template>

    <PageFooter />
  </div>
</template>

<style scoped>
.course-detail-page {
  min-height: 100vh;
  background: #141428;
  color: rgba(255, 255, 255, 0.92);
}

.state-msg {
  text-align: center;
  padding: 120px 0;
  color: rgba(255, 255, 255, 0.4);
}

.back-btn {
  margin-top: 16px;
  background: transparent;
  border: 1px solid #e94560;
  color: #e94560;
  padding: 8px 24px;
  cursor: pointer;
  border-radius: 4px;
}

/* ===== 头部 ===== */
.hero-section {
  position: relative;
  height: 360px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.hero-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 6rem;
  color: rgba(255, 255, 255, 0.08);
  background: linear-gradient(135deg, #1e2a4a, #2a1a3e);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(0deg, #141428 0%, rgba(20, 20, 40, 0.6) 60%, transparent 100%);
}

.hero-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 32px 48px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 8px;
}

.hero-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
  margin-bottom: 16px;
}

.hero-meta {
  display: flex;
  gap: 20px;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 20px;
}

.hero-price {
  display: flex;
  align-items: center;
  gap: 16px;
}

.price {
  font-size: 1.8rem;
  font-weight: 700;
  color: #e94560;
}

.price.free { color: #27ae60; font-size: 1.4rem; }

.original {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.35);
  text-decoration: line-through;
  margin-left: 8px;
}

.buy-btn {
  background: #e94560;
  color: #fff;
  border: none;
  padding: 12px 36px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  letter-spacing: 1px;
  transition: background 0.2s;
}

.buy-btn:hover {
  background: #d63850;
}

.cart-add-btn {
  background: transparent;
  border: 1px solid #e94560;
  color: #e94560;
  padding: 12px 36px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all 0.2s;
}

.cart-add-btn:hover {
  background: #e94560;
  color: #fff;
}

/* ===== 主体 ===== */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 48px 80px;
  display: flex;
  gap: 40px;
}

.content-left {
  flex: 1;
  min-width: 0;
}

.content-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.description {
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
}

/* 章节列表 */
.chapter-item {
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  margin-bottom: 12px;
  overflow: hidden;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  background: rgba(255, 255, 255, 0.04);
  cursor: pointer;
}

.chapter-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.chapter-meta {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}

.lesson-list {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.lesson-item {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  gap: 12px;
  font-size: 0.9rem;
  transition: background 0.2s;
  cursor: pointer;
}

.lesson-item:hover {
  background: rgba(255, 255, 255, 0.04);
}

.lesson-index {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
  flex-shrink: 0;
}

.lesson-title {
  flex: 1;
  color: rgba(255, 255, 255, 0.8);
}

.lesson-preview {
  font-size: 0.7rem;
  padding: 1px 8px;
  border-radius: 3px;
  background: #27ae60;
  color: #fff;
  flex-shrink: 0;
}

.lesson-duration {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
  flex-shrink: 0;
}

/* 侧边信息卡 */
.info-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 20px;
  position: sticky;
  top: 20px;
}

.info-card h3 {
  font-size: 1rem;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 0.85rem;
}

.info-label {
  color: rgba(255, 255, 255, 0.5);
}

.info-value {
  color: rgba(255, 255, 255, 0.85);
}
</style>
