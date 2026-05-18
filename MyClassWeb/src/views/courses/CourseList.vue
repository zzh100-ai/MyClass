<script setup>
import { ref, onMounted, watch } from 'vue'
import { useCourseStore } from '@/stores/courses'
import CourseCard from '@/components/courses/CourseCard.vue'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const courseStore = useCourseStore()

const activeCategory = ref('')

onMounted(() => {
  courseStore.fetchCategories()
  courseStore.fetchCourses()
})

watch(activeCategory, (val) => {
  courseStore.setPage(1)
  courseStore.fetchCourses({ category: val || undefined })
})

function onPageChange(page) {
  courseStore.setPage(page)
  courseStore.fetchCourses({ category: activeCategory.value || undefined })
}
</script>

<template>
  <div class="course-list-page">
    <NavBar />

    <main class="main-content">
      <div class="page-header">
        <h1 class="page-title">全部课程</h1>
        <p class="page-desc">体系化课程，从入门到精通</p>
      </div>

      <!-- 分类筛选 -->
      <div class="category-bar">
        <button
          :class="['cat-btn', { active: !activeCategory }]"
          @click="activeCategory = ''"
        >全部</button>
        <button
          v-for="cat in courseStore.categories"
          :key="cat.id"
          :class="['cat-btn', { active: activeCategory === String(cat.id) }]"
          @click="activeCategory = String(cat.id)"
        >{{ cat.name }}</button>
      </div>

      <!-- TODO: 课程列表渲染
             实现：
             1. 加载态显示骨架屏或 loading 文字
             2. 空数据时显示"暂无课程"
             3. 课程卡片点击跳转到详情页
      -->

      <!-- 加载中 -->
      <div v-if="courseStore.loading" class="state-msg">加载中...</div>

      <!-- 空状态 -->
      <div v-else-if="courseStore.courses.length === 0" class="state-msg">
        暂无课程
      </div>

      <!-- 课程网格 -->
      <div v-else class="course-grid">
        <CourseCard
          v-for="course in courseStore.courses"
          :key="course.id"
          :course="course"
        />
      </div>

      <!-- 分页 -->
      <div v-if="courseStore.totalPages > 1" class="pagination">
        <button
          :disabled="courseStore.currentPage <= 1"
          @click="onPageChange(courseStore.currentPage - 1)"
        >上一页</button>
        <span class="page-info">
          {{ courseStore.currentPage }} / {{ courseStore.totalPages }}
        </span>
        <button
          :disabled="courseStore.currentPage >= courseStore.totalPages"
          @click="onPageChange(courseStore.currentPage + 1)"
        >下一页</button>
      </div>
    </main>

    <PageFooter />
  </div>
</template>

<style scoped>
.course-list-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #1a1a3e 0%, #1e2a4a 30%, #1c2541 60%, #1a1a3e 100%);
  color: rgba(255, 255, 255, 0.94);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 48px 80px;
}

.page-header {
  text-align: center;
  margin-bottom: 36px;
}

.page-title {
  font-size: 2rem;
  font-weight: 600;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

.page-desc {
  color: rgba(255, 255, 255, 0.55);
  font-size: 0.9rem;
}

/* 分类栏 */
.category-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 36px;
}

.cat-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.cat-btn:hover {
  border-color: rgba(233, 69, 96, 0.3);
  color: #fff;
}

.cat-btn.active {
  background: #e94560;
  border-color: #e94560;
  color: #fff;
}

/* 课程网格 */
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* 状态信息 */
.state-msg {
  text-align: center;
  padding: 80px 0;
  color: rgba(255, 255, 255, 0.4);
  font-size: 1rem;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 48px;
}

.pagination button {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  padding: 8px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination button:hover:not(:disabled) {
  border-color: #e94560;
  color: #e94560;
}

.pagination button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}
</style>
