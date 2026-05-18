"""
缓存工具与常量

Redis 配置见 config/settings.py 中 CACHES 配置:
  - default: 通用缓存
  - courses: 课程模块专用缓存（当前正在使用的）

用法:
  from django.core.cache import caches
  course_cache = caches['courses']
"""

# ---------- 缓存键定义 ----------
# 键名格式: 模块:业务:参数
# 使用 {param} 占位符，调用时用 .format() 填充

# 课程列表缓存，category=all 表示全部，其他值为分类ID
CACHE_KEY_COURSE_LIST = "courses:list:{category}"
# 课程详情缓存，course_id 为课程主键
CACHE_KEY_COURSE_DETAIL = "courses:detail:{course_id}"

# ---------- 缓存过期时间 ----------
# 课程列表缓存 15 分钟
CACHE_TTL_LIST = 60 * 15
# 课程详情缓存 30 分钟，而且存储到了第0个redis库中
CACHE_TTL_DETAIL = 60 * 30

# ---------- 缓存别名 ----------
# settings.py 中为课程模块配置了独立的 Redis 连接，这里指定其别名
COURSE_CACHE_ALIAS = "courses"
