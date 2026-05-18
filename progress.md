# 开发进度日志

## 会话 1 (2026-05-14)
- 创建规划文件
- 整理已有工作：课程 app 的模型、序列化器、视图（部分）、settings 配置、urls 挂载
- **已完成**：课程 API 完善
  - 添加自定义权限 IsTeacherOrReadOnly（教师可写，其他只读）
  - 实现课程详情嵌套序列化：课程详情返回包含章节和课时的完整结构
  - 注册 router，API 路由生效
  - 为所有视图集应用合适的权限
- 下一步：阶段2完成，可测试 API；准备进入阶段3（课程搜索 - Elasticsearch）

## 测试结果
- 创建课程 API：❌ teacher 字段被要求必填、cover_image 期望文件对象

## 遇到的问题与解决
1. **teacher 字段必填错误** — 序列化器中 teacher 未设 read_only，DRF 默认要求客户端传递外键 ID。已在 CourseSerializer 中显式添加 `teacher = serializers.PrimaryKeyRelatedField(read_only=True)`，由 perform_create 自动赋值当前用户。
2. **cover_image 非文件错误** — ImageField 默认不接受 JSON 中的 null 值。已改为 `allow_null=True`，允许创建时不传封面图。轻量需求下后续可改为 CharField 存储 URL。

## 会话 2 (2026-05-18)
- 搭建搜索模块框架（apps/search/）
- 创建 CourseDocument ES 文档定义（IK 分词器）
- 创建搜索 API 框架（SearchView + Serializer）
- 创建热词统计框架（Redis ZSET）
- TODO 标注核心查询逻辑，由用户实现

## 会话 3 (2026-05-18)
- 搭建购物车模块（apps/cart/）
- 创建 Redis Hash 函数框架（redis_cart.py）
- 创建购物车 API 框架（CartViewSet + Serializer）
- TODO 标注核心 CRUD 逻辑，由用户实现
