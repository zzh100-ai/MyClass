# 购物车 API（Redis Hash）

## 添加课程

```
POST /api/v1/cart/
Authorization: Bearer <access_token>
Content-Type: application/json

Body:
{
    "course_id": 1
}

Response 201:
{
    "msg": "已添加到购物车"
}

Response 200（已在购物车中）:
{
    "msg": "课程已在购物车中"
}
```

## 购物车列表

```
GET /api/v1/cart/
Authorization: Bearer <access_token>

Response 200:
[
    {
        "id": 1,
        "title": "Python 入门到精通",
        "cover_image": "/media/covers/python.jpg",
        "price": "199.00",
        "is_free": false,
        "teacher_name": "张三老师"
    }
]
```

## 移除课程

```
DELETE /api/v1/cart/{course_id}/
Authorization: Bearer <access_token>

Response 204: 无内容
Response 404: {"msg": "课程不在购物车中"}
```

## 清空购物车

```
DELETE /api/v1/cart/clear/
Authorization: Bearer <access_token>

Response 204: 无内容
```

## 购物车数量

```
GET /api/v1/cart/count/
Authorization: Bearer <access_token>

Response 200:
{
    "count": 3
}
```

## 业务规则

- 使用 Redis Hash 存储，键为 `cart:{user_id}`，field 为 course_id
- 每门课程在购物车中只能存在一份（重复添加返回已存在）
- 所有接口需要 JWT 认证（购物车绑定用户）
