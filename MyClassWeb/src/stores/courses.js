import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as coursesApi from '@/api/courses'

export const useCourseStore = defineStore('courses', () => {
  // ===== 状态 =====
  const courses = ref([])           // 课程列表数据
  const currentCourse = ref(null)   // 当前查看的课程详情
  const categories = ref([])        // 分类列表
  const loading = ref(false)        // 列表加载状态
  const detailLoading = ref(false)  // 详情加载状态
  const total = ref(0)              // 课程总数（用于分页）
  const currentPage = ref(1)
  const pageSize = ref(20)

  // ===== 计算属性 =====
  const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

  // ===== 动作 =====

  /** 获取课程列表 */
  async function fetchCourses(params = {}) {
    loading.value = true
    try {
      const res = await coursesApi.getCourses({
        page: currentPage.value,
        page_size: pageSize.value,
        ...params,
      })
      // TODO: 处理响应数据并更新 courses 和 total
      // res 格式: { count, next, previous, results }
      courses.value = res.results
      total.value = res.count
    } catch (e) {
      console.error('获取课程列表失败:', e.message)
      courses.value = []
    } finally {
      loading.value = false
    }
  }

  /** 获取课程详情 */
  async function fetchCourse(id) {
    detailLoading.value = true
    currentCourse.value = null
    try {
      const res = await coursesApi.getCourse(id)
      currentCourse.value = res
    } catch (e) {
      console.error('获取课程详情失败:', e.message)
    } finally {
      detailLoading.value = false
    }
  }

  /** 获取分类列表 */
  async function fetchCategories() {
    try {
      const res = await coursesApi.getCategories()
      categories.value = res
    } catch (e) {
      console.error('获取分类失败:', e.message)
    }
  }

  /** 设置当前页 */
  function setPage(page) {
    currentPage.value = page
  }

  return {
    courses,
    currentCourse,
    categories,
    loading,
    detailLoading,
    total,
    currentPage,
    pageSize,
    totalPages,
    fetchCourses,
    fetchCourse,
    fetchCategories,
    setPage,
  }
})
