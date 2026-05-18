<script setup>
defineProps({
  course: { type: Object, required: true },
})
</script>

<template>
  <div class="course-card" @click="$router.push(`/courses/${course.id}`)">
    <!-- 封面图 -->
    <div class="card-image">
      <img
        v-if="course.cover_image"
        :src="course.cover_image"
        :alt="course.title"
      />
      <div v-else class="card-placeholder">{{ course.title?.[0] || '课' }}</div>
      <!-- 状态标签 -->
      <span v-if="course.is_free" class="card-tag free">免费</span>
      <span v-else-if="course.original_price" class="card-tag sale">优惠</span>
    </div>

    <!-- 课程信息 -->
    <div class="card-body">
      <h3 class="card-title">{{ course.title }}</h3>
      <p class="card-desc">{{ course.subtitle || course.description?.replace(/<[^>]+>/g, '').slice(0, 60) }}</p>

      <div class="card-meta">
        <span class="card-teacher">{{ course.teacher_name }}</span>
        <span class="card-students">{{ course.learn_count }} 人学习</span>
      </div>

      <div class="card-footer">
        <span v-if="course.is_free" class="card-price free">免费</span>
        <span v-else class="card-price">
          ¥{{ course.price }}
          <span v-if="course.original_price" class="card-original">¥{{ course.original_price }}</span>
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.course-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}
.course-card:hover {
  transform: translateY(-4px);
  border-color: rgba(233, 69, 96, 0.3);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.card-image {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.04);
}
.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.card-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.15);
  background: linear-gradient(135deg, #1e2a4a, #2a1a3e);
}

.card-tag {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 2px 10px;
  border-radius: 3px;
  font-size: 0.75rem;
  letter-spacing: 1px;
}
.card-tag.free { background: #27ae60; color: #fff; }
.card-tag.sale { background: #e94560; color: #fff; }

.card-body {
  padding: 16px;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 8px;
  color: rgba(255, 255, 255, 0.92);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-desc {
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.55);
  margin: 0 0 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.card-footer {
  display: flex;
  align-items: center;
}

.card-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: #e94560;
}
.card-price.free { color: #27ae60; }

.card-original {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.35);
  text-decoration: line-through;
  font-weight: 400;
  margin-left: 6px;
}
</style>
