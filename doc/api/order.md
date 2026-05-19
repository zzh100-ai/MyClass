# 订单 API

## 创建订单（从购物车结算）

```
POST /api/v1/orders/
Authorization: Bearer <access_token>
Content-Type: application/json

Body:
{
    "course_ids": [1, 2, 3],
    "coupon_id": 1,       // 可选，用户优惠券ID
    "points": 100         // 可选，使用的积分数
}

Response 201:
{
    "id": 1,
    "order_no": "20260518132710173829",
    "total_amount": "498.00",
    "final_amount": "448.00",
    "coupon_discount": "50.00",
    "points_discount": "0.00",
    "points_used": 0,
    "status": "pending",
    "items": [
        {"id": 1, "course": 1, "course_title": "Python 入门到精通", "price": "199.00"},
        {"id": 2, "course": 2, "course_title": "Java 高级编程", "price": "299.00"}
    ],
    "created_at": "2026-05-18T13:27:10Z",
    "paid_at": null
}
```

## 订单列表

```
GET /api/v1/orders/
Authorization: Bearer <access_token>

Response 200:
{
    "count": 10,
    "results": [ 同订单详情结构 ]
}
```

## 订单详情

```
GET /api/v1/orders/{id}/
Authorization: Bearer <access_token>

Response 200: 同创建订单的返回结构
```

## 模拟支付

```
POST /api/v1/orders/{id}/pay/
Authorization: Bearer <access_token>

Response 200:
{
    "msg": "支付成功",
    "order_no": "20260518132710173829"
}

Response 400:
{
    "msg": "订单状态不允许支付"
}
```

## 支付回调

```
POST /api/v1/orders/notify/
Content-Type: application/json

Body:
{
    "order_no": "20260518132710173829",
    "status": "paid"
}

Response 200:
{
    "msg": "success"
}
```

## 业务规则

- 创建订单时自动计算优惠券减免和积分抵扣
- 支付后自动扣减积分、标记优惠券已使用、从购物车移除已购课程
- 只能创建 **pending** 状态的订单；已支付不能再次支付
- 重复下单检查：同课程有待支付订单或已购买时阻止
