# 优惠券和积分 API

## 优惠券模板（管理员）

```
GET /api/v1/coupons/          → 列表
POST /api/v1/coupons/         → 创建
GET /api/v1/coupons/{id}/     → 详情
PUT /api/v1/coupons/{id}/     → 更新
DELETE /api/v1/coupons/{id}/  → 删除
Authorization: Bearer <admin_token>

响应结构:
{
    "id": 1,
    "code": "NEWUSER50",
    "name": "新用户立减50",
    "discount_type": "fixed",
    "discount_value": "50.00",
    "min_amount": "0.00",
    "valid_from": "2026-01-01T00:00:00Z",
    "valid_to": "2026-12-31T23:59:59Z",
    "is_active": true,
    "total_count": 1000,
    "used_count": 0,
    "remaining": 1000,
    "description": "新用户专享优惠券"
}
```

## 我的优惠券

```
GET /api/v1/user-coupons/
Authorization: Bearer <access_token>

Response 200:
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "coupon": { ... 同优惠券模板结构 },
            "status": "unused",
            "received_at": "2026-05-18T10:00:00Z",
            "used_at": null
        }
    ]
}
```

## 领取优惠券

```
POST /api/v1/user-coupons/collect/
Authorization: Bearer <access_token>
Content-Type: application/json

Body:
{
    "code": "NEWUSER50"
}

Response 201:
{
    "id": 1,
    "coupon": { ... },
    "status": "unused",
    "received_at": "...",
    "used_at": null
}
```

## 积分余额

```
GET /api/v1/points/
Authorization: Bearer <access_token>

Response 200:
{
    "points": 500
}
```

## 积分流水

```
GET /api/v1/points/history/?page=1&page_size=20
Authorization: Bearer <access_token>

Response 200:
{
    "total": 5,
    "results": [
        {
            "id": 3,
            "amount": -100,
            "balance": 400,
            "type": "redeem",
            "description": "订单20260518132710173829积分抵扣",
            "created_at": "..."
        }
    ]
}
```

## 业务规则

- 优惠券类型：`fixed`（固定金额减免）和 `percent`（百分比折扣）
- 领取限制：每个用户同一券码只能领取一次
- 优惠券状态流转：`unused` → `used` / `expired`
- 积分抵扣比例：1 积分 = ¥0.01
- 积分流水类型：`register` / `purchase` / `redeem` / `refund` / `expire`
- 优惠券需满足 `min_amount`（最低消费金额）才能使用
- 管理员后台可批量发放优惠券给指定用户
