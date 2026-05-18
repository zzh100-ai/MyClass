"""
购物车 — Redis Hash 存储

数据结构:
  Hash Key: "cart:{user_id}"
  Hash Field: course_id (字符串)
  Hash Value: JSON 字符串 {"added_at": "..."}

Redis Hash 命令:
  HSET key field value    → 添加/更新（field 不存在则创建，存在则覆盖）
  HDEL key field          → 删除指定 field
  HGETALL key             → 获取所有 field-value
  HLEN key                → 获取 field 数量
  DEL key                 → 删除整个 key

理解以下内容
  1. Hash 与 String 的区别，为什么购物车用 Hash 不用 String？
  2. HSET 和 HMSET 的区别？
  3. HGETALL 在 field 很多时的性能问题
"""

import json
from datetime import datetime

# Key 前缀
CART_KEY_PREFIX = "cart:{user_id}"


def get_cart_key(user_id):
    """生成 Redis Hash 键名"""
    return CART_KEY_PREFIX.format(user_id=user_id)


def add_course(cart_redis, user_id, course_id):
    """
    添加课程到购物车
    实现 Redis Hash 添加
      1. 生成 cart_key: cart:{user_id}
      2. 检查该课程是否已在购物车中: cart_redis.hexists(key, course_id)
      3. 如果已存在，直接返回（不重复添加）
      4. 如果不存在，用 HSET 写入: value = json.dumps({"added_at": now_iso})
    """
    key = get_cart_key(user_id)
    if cart_redis.hexists(key, course_id):
        return False  # 已经在购物车中
    # 不存在则添加
    value = json.dumps({"added_at": datetime.now().isoformat()})
    cart_redis.hset(key, course_id, value)
    return True


def remove_course(cart_redis, user_id, course_id):
    """
    从购物车移除课程
    实现 Redis Hash 删除
      1. cart_redis.hdel(key, course_id)
      2. 返回是否删除成功（HDEL 返回受影响的 field 数量）
    """
    key = get_cart_key(user_id)
    result = cart_redis.hdel(key, course_id)
    return result > 0  # 返回 True 表示删除成功


def list_courses(cart_redis, user_id):
    """
    获取购物车中所有课程 ID 列表
    实现 Redis Hash 全量获取
      1. cart_redis.hgetall(key) → 返回 {field: value, ...}
      2. field 就是 course_id（但 Redis 返回的是 bytes）
      3. 提取所有 course_id，组装成列表 [1, 2, 3, ...]
      4. value 可以暂时忽略（后续可用于排序）

    返回: [course_id, course_id, ...] 按添加时间倒序排列
          或空列表 []
    """
    key = get_cart_key(user_id)
    data = cart_redis.hgetall(key)
    if not data:
        return []
    # 提取所有 course_id
    cart_items = []
    for field, value in data.items():
        course_id = int(field.decode() if isinstance(field, bytes) else field)
        cart_items.append(course_id)
    return cart_items


def clear_cart(cart_redis, user_id):
    """
    清空购物车

    实现
      1. cart_redis.delete(key)
    """
    key = get_cart_key(user_id)
    cart_redis.delete(key)


def get_cart_count(cart_redis, user_id):
    """
    获取购物车中课程数量

    实现
      1. cart_redis.hlen(key) → 返回 field 数量
      2. 如果 key 不存在，HLEN 返回 0
    """
    key = get_cart_key(user_id)
    return cart_redis.hlen(key)
