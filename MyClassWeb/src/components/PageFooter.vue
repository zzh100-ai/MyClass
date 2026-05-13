<script setup>
// 通用页脚组件
</script>

<template>
  <footer class="footer">
    <div class="footer-line"></div>
    <p>持续学习，终身成长</p>
    <p class="footer-sub">Learning is a lifelong journey</p>
  </footer>
</template>

<style scoped>
.footer {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 60px 20px 40px;
}

.footer-line {
  width: 40px;
  height: 1px;
  background: #e94560;
  margin: 0 auto 20px;
}

.footer p {
  margin: 0;
  color: rgba(255, 255, 255, 0.55);
  font-size: 0.85rem;
  letter-spacing: 2px;
}

.footer-sub {
  margin-top: 6px;
  font-size: 0.7rem;
  opacity: 0.5;
  font-style: italic;
  letter-spacing: 1px;
}
</style>
