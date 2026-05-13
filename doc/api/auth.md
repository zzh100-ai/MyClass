# 认证 API

## 注册

```
POST /api/v1/auth/register/
Content-Type: application/json

Body:
{
    "username": "testuser",
    "password": "Abcd1234",
    "password2": "Abcd1234",
    "email": "test@test.com",
    "mobile": "13800138000"
}

Response 201:
{
    "code": 200,
    "msg": "注册成功",
    "data": {
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@test.com",
            "mobile": "13800138000",
            "date_joined": "..."
        },
        "access": "<JWT access token>",
        "refresh": "<JWT refresh token>"
    }
}

Response 400:
{
    "code": 400,
    "msg": "参数错误",
    "errors": {
        "password": ["密码必须包含字母"],
        "mobile": ["手机号格式错误"]
    }
}
```

## 登录

支持用户名、手机号、邮箱任意一种方式登录。

```
POST /api/v1/auth/login/
Content-Type: application/json

Body:
{
    "identifier": "testuser",   // 用户名/手机号/邮箱
    "password": "Abcd1234"
}

Response 200:
{
    "code": 200,
    "msg": "登录成功",
    "data": {
        "user": { ... },
        "access": "<JWT access token>",
        "refresh": "<JWT refresh token>"
    }
}

Response 400（密码错误）:
{
    "code": 400,
    "msg": "参数错误",
    "errors": {
        "non_field_errors": ["用户名或密码错误，剩余4次尝试"]
    }
}

Response 400（失败次数超限）:
{
    "code": 400,
    "msg": "参数错误",
    "errors": {
        "non_field_errors": ["登录失败次数过多，请15分钟后再试"]
    }
}
```

## 刷新 Token

```
POST /api/v1/auth/refresh/
Content-Type: application/json

Body:
{
    "refresh": "<refresh token>"
}

Response 200:
{
    "code": 200,
    "msg": "刷新成功",
    "data": {
        "access": "<new access token>",
        "refresh": "<new refresh token>"
    }
}

Response 401（token 已失效或被使用过）:
{
    "code": 401,
    "msg": "refresh token 已过期"
}
```

## Token 说明

在需要认证的 API 请求中加入 Header：

```
Authorization: Bearer <access token>
```

| 配置项 | 值 |
|--------|-----|
| Access token 有效期 | 30 分钟 |
| Refresh token 有效期 | 7 天 |
| 刷新轮换 | 每次刷新签发新 token，旧的立即失效（Redis 白名单） |
| 登录失败限制 | 5 次/15 分钟 |
