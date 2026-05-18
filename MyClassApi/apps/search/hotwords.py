"""
搜索热词统计 — 基于 Redis ZSET

Redis ZSET 命令:
  - ZINCRBY hotwords 1 "关键词"   → 加热度（+1）
  - ZREVRANGE hotwords 0 9 WITHSCORES → 获取热度最高的10个词
  - ZREMRANGEBYRANK hotwords 0 -101  → 只保留前100个（定期清理）
"""

# Redis ZSET 键名
HOTWORDS_KEY = "search:hotwords"

# 排行榜展示数量
HOTWORDS_TOP_N = 10

# ZSET 最大容量
HOTWORDS_MAX_SIZE = 100

# TODO: 实现热词统计逻辑
#   1. 每次搜索成功后调用 record_search(keyword) 记录
#   2. get_top_hotwords() 获取前10热门搜索词
#   3. 定期调用 trim_hotwords() 清理冷门词，保持 ZSET 不超过 100 条
