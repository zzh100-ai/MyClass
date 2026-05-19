# API 文档

## 约定

- 基础路径：`http://localhost:8000/api/v1/`
- 数据格式：JSON
- 认证方式：JWT（Bearer Token），通过 SimpleJWT 实现

## 接口列表

### 认证模块

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/register/` | 用户注册 |
| POST | `/api/v1/auth/login/` | 用户登录 |
| POST | `/api/v1/auth/refresh/` | 刷新 Token |

> 详细请求/响应示例见 [auth.md](auth.md)

### 课程模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/courses/` | 课程列表 |
| GET | `/api/v1/courses/{id}/` | 课程详情 |
| POST | `/api/v1/courses/` | 创建课程 |
| PUT/PATCH | `/api/v1/courses/{id}/` | 更新课程 |
| DELETE | `/api/v1/courses/{id}/` | 删除课程 |
| GET | `/api/v1/categories/` | 分类列表 |
| POST | `/api/v1/categories/` | 创建分类 |
| GET | `/api/v1/chapters/` | 章节列表 |
| POST | `/api/v1/chapters/` | 创建章节 |
| GET | `/api/v1/lessons/` | 课时列表 |
| POST | `/api/v1/lessons/` | 创建课时 |

> 详细请求/响应示例见 [courses.md](courses.md)

### 购物车模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/cart/` | 购物车列表 | JWT |
| POST | `/api/v1/cart/` | 添加课程 | JWT |
| DELETE | `/api/v1/cart/{course_id}/` | 移除课程 | JWT |
| DELETE | `/api/v1/cart/clear/` | 清空购物车 | JWT |
| GET | `/api/v1/cart/count/` | 购物车数量 | JWT |

> 详细请求/响应示例见 [cart.md](cart.md)

### 订单模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/orders/` | 创建订单 | JWT |
| GET | `/api/v1/orders/` | 订单列表 | JWT |
| GET | `/api/v1/orders/{id}/` | 订单详情 | JWT |
| POST | `/api/v1/orders/{id}/pay/` | 模拟支付 | JWT |
| POST | `/api/v1/orders/notify/` | 支付回调 | - |

> 详细请求/响应示例见 [order.md](order.md)

### 优惠券和积分模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/coupons/` | 优惠券模板列表 | Admin |
| POST | `/api/v1/coupons/` | 创建优惠券模板 | Admin |
| GET | `/api/v1/user-coupons/` | 我的优惠券 | JWT |
| POST | `/api/v1/user-coupons/collect/` | 领取优惠券 | JWT |
| GET | `/api/v1/points/` | 积分余额 | JWT |
| GET | `/api/v1/points/history/` | 积分流水 | JWT |

> 详细请求/响应示例见 [coupon.md](coupon.md)
