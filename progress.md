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

## 会话 4 (2026-05-19)
- **优惠券模块（apps/coupon/）** — 完整实现
  - 数据模型：Coupon（优惠券模板）、UserCoupon（用户领取记录）、PointsTransaction（积分流水）
  - 定价引擎（pricing.py）：活动-优惠类型-公式三层抽象，支持满减/折扣/积分抵扣组合
  - API：CouponViewSet（管理员CRUD）、UserCouponViewSet（用户领取+列表）、PointsViewSet（余额+流水）
  - 前端：CouponList.vue、coupon store、coupon API
- **订单模块（apps/order/）** — 完整实现
  - 数据模型：Order（含订单号生成、状态字段）、OrderItem（价格快照）
  - 创建订单：集成了优惠券/积分计算、清空购物车
  - 模拟支付：pay 接口 + notify 回调 + _handle_payment_success 统一处理
  - 支付成功处理：扣减积分、标记优惠券已用、清空购物车
  - 前端：CheckoutPage.vue、OrderList.vue、OrderDetail.vue、order store
- **用户模型扩展：** 添加 points 积分字段，迁移文件已生成
- **前端路由与导航：** 所有页面路由配置完成，NavBar 链接完善
- **文档：** cart.md、coupon.md、order.md API 文档编写完成

## 总体进度（2026-05-19）

| 模块 | 状态 | 说明 |
|------|------|------|
| 阶段1 基础架构 | ✅ 完成 | Django + DRF + JWT + Redis + MySQL |
| 阶段2 课程模块 | ✅ 完成 | 模型/序列化器/视图/权限 |
| 阶段3 ES搜索 | ⚠️ 框架 | 需安装 ES 服务 + 补全 TODO |
| 阶段4 购物车 | ✅ 完成 | Redis Hash + API + 前端 |
| 阶段5 优惠券/积分 | ✅ 完成 | 模型/定价引擎/API/前端 |
| 阶段6 订单/支付 | ✅ 完成 | 订单/支付/回调/前端 |
| 阶段7 Celery | ⏸️ 待开始 | — |
| 阶段8 前端集成 | ✅ 完成 | 随模块同步开发 |
| 阶段9 部署 | ⏸️ 待开始 | — |
