# SimpleJWT 详细教程

## 一、什么是 JWT

JWT（JSON Web Token）由三部分组成，用 `.` 分隔：

```
header.payload.signature
eyJ0eXAiOiJKV1Qi.eyJ1c2VyX2lkIjoxfQ.HMAC_SHA256签名
```

- **Header：** 算法类型（HS256 / RS256）
- **Payload：** 实际数据（user_id、过期时间、自定义字段），Base64 编码，**不加密**，任何人可解码读取
- **Signature：** 签名 = HMAC(header + "." + payload, SECRET_KEY)，防止篡改

SimpleJWT 是 Django REST Framework 的 JWT 插件，提供两个 token：

| Token 类型 | 默认有效期 | 用途 |
|-----------|-----------|------|
| Access Token | 30 分钟 | 携带在请求头中，用于鉴权 |
| Refresh Token | 7 天 | 仅用于获取新的 Access Token |

## 二、配置详解

```python
# config/settings.py
from datetime import timedelta

SIMPLE_JWT = {
    # Token 有效期
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),      # 访问令牌
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),         # 刷新令牌

    # 刷新时是否轮换 Refresh Token
    # True：每次刷新都发新的 refresh token，旧的作废
    # False：refresh token 不变，只能刷一次
    "ROTATE_REFRESH_TOKENS": True,

    # 轮换后是否将旧的 refresh token 加入黑名单
    # 需要启用 blacklist app（后面讲）
    "BLACKLIST_AFTER_ROTATION": False,

    # 请求头中 Authorization 的前缀
    "AUTH_HEADER_TYPES": ("Bearer",),

    # 用户模型路径
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",

    # 签名算法
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}
```

## 三、Token 的创建与使用

### 3.1 签发 Token

```python
from rest_framework_simplejwt.tokens import RefreshToken

# 为指定用户生成一对 token
refresh = RefreshToken.for_user(user)

# 获取 access token（字符串）
access_token = str(refresh.access_token)

# 获取 refresh token（字符串）
refresh_token = str(refresh)
```

### 3.2 Token 内部结构

`RefreshToken` 是个类字典对象，可以直接访问 payload 中的字段：

```python
refresh = RefreshToken.for_user(user)

print(refresh["user_id"])          # 1（用户 ID）
print(refresh["jti"])              # "abc123..."（JWT ID，全局唯一）
print(refresh["token_type"])       # "refresh"
print(refresh["exp"])              # 过期时间戳

# access token 也是类似结构
print(refresh.access_token["token_type"])  # "access"
```

### 3.3 客户端使用 Token

前端请求需要认证的接口时，在 Header 中携带：

```
Authorization: Bearer <access_token>
```

### 3.4 服务端验证 Token

SimpleJWT 的 `JWTAuthentication` 中间件会自动从 Header 解析 token、验证签名和有效期：

```python
# 在视图中获取当前用户
request.user   # 已认证 → User 对象，未认证 → AnonymousUser
request.auth   # 解码后的 token payload
```

## 四、自定义 Token 载荷

有时需要把额外信息放入 JWT payload 中，比如用户角色、昵称等。

### 方式一：每个 Token 类单独定义

适用场景：只在某个特定签发需求中加字段。

在视图中动态添加：
```python
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        # 添加自定义字段
        refresh["role"] = user.role           # 用户角色
        refresh["nickname"] = user.username   # 昵称

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })

# 读取时
refresh = RefreshToken(token_string)
print(refresh["role"])  # "admin"
```

### 方式二：全局自定义 Token 类

适用场景：给所有 token 自动注入相同的额外字段。

在 `apps/users/` 下创建 `tokens.py`：

```python
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class MyToken(RefreshToken):
    """自定义 Token：自动注入额外载荷"""

    def for_user(cls, user):
        """重写 for_user 方法，添加自定义字段"""
        token = super().for_user(user)
        token["mobile"] = user.mobile
        return token
```

然后在视图中用 `MyToken.for_user(user)` 替代 `RefreshToken.for_user(user)`。

### 方式三：通过 signal 注入

在拿到 token 对象后、返回给客户端前加字段（本项目当前的方式）。

### 从 payload 中读取自定义字段

```python
# 在任何视图中通过 request.auth 读取
class SomeView(APIView):
    def get(self, request):
        user_id = request.auth.get("user_id")     # SimpleJWT 默认字段
        role = request.auth.get("role")           # 自定义字段
```

## 五、自定义返回格式

SimpleJWT 内置视图返回的格式是 `{"access": "...", "refresh": "..."}`，与项目统一的 `{code, msg, data}` 不一致。需要包装。

### TokenRefreshView

```python
from rest_framework_simplejwt.views import TokenRefreshView

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # 调用父类获取原始响应
        response = super().post(request, *args, **kwargs)

        # 包装成统一格式
        return Response({
            "code": 200,
            "msg": "刷新成功",
            "data": {
                "access": response.data.get("access"),
                "refresh": response.data.get("refresh"),
            }
        })
```

### TokenObtainPairView（登录）

如果不用自定义 LoginView，而是用 SimpleJWT 内置的 TokenObtainPairView，同样需要包装：

```python
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            "code": 200,
            "msg": "登录成功",
            "data": response.data,
        })
```

不过本项目已经用 `LoginView(APIView)` 完全自定义了登录流程，不需要这个。

## 六、Token 黑名单（作废机制）

`ROTATE_REFRESH_TOKENS=True` 时，每次刷新会签发新 token。如果不做处理，旧的 refresh token 理论上还能用（因为还没过期）。SimpleJWT 提供 blacklist app 来自动作废。

### 启用步骤：

1. `INSTALLED_APPS` 添加 `"rest_framework_simplejwt.token_blacklist"`
2. `SIMPLE_JWT` 中设置 `"BLACKLIST_AFTER_ROTATION": True`
3. `python manage.py migrate` 创建黑名单表

这样每次刷新后，旧的 refresh token 会被写入数据库黑名单，无法再次使用。

### 本项目用的是 Redis 白名单方案（而非数据库黑名单）

区别：
- **黑名单**：默认所有 token 有效，只拒绝黑名单里的。SimpleJWT 内置，存 MySQL。
- **白名单**：默认所有 token 无效，只接受白名单里的。自行实现，存 Redis，性能更高。

本项目选择白名单，将有效的 refresh token 的 `jti`（JWT ID）存入 Redis，刷新时验证 → 删除旧的 → 写入新的。

## 七、常见开发流程总结

### 注册流程

```
客户端                   服务端
  │                       │
  │── POST /register ────→│
  │   {username,password, │  ① serializer 验证字段
  │    password2,email,   │  ② 创建 User（密码加密）
  │    mobile}            │  ③ RefreshToken.for_user(user)
  │                       │  ④ Redis 白名单存入 refresh jti
  │←── 201 {user,tokens}─ │
```

### 登录流程

```
客户端                   服务端
  │                       │
  │── POST /login ───────→│
  │   {identifier,        │  ① 检查失败计数器（Redis）
  │    password}          │  ② 多字段查询用户
  │                       │  ③ check_password 校验
  │                       │  ④ 失败 → INCR 计数器
  │                       │  ⑤ 成功 → DELETE 计数器
  │                       │  ⑥ 签发 token → 白名单
  │←── 200 {user,tokens}─ │
```

### 刷新流程

```
客户端                   服务端
  │                       │
  │── POST /refresh ─────→│
  │   {refresh: "旧的"}   │  ① 解码旧 token，取 jti
  │                       │  ② Redis EXISTS 查白名单
  │                       │  ③ 不在 → 401
  │                       │  ④ 在 → DELETE 旧的
  │                       │  ⑤ 签发新 token
  │                       │  ⑥ Redis SET 新的 jti
  │←── 200 {新 tokens}─── │
```

### 鉴权流程（任意受保护接口）

```
客户端                   服务端
  │                       │
  │── GET /api/xxx ──────→│
  │   Authorization:      │  ① JWTAuthentication 解析 Header
  │   Bearer <access>     │  ② 验证签名（SECRET_KEY）
  │                       │  ③ 验证有效期（exp）
  │                       │  ④ 通过 → request.user = User
  │                       │  ⑤ 不通过 → 401
  │←── 200 {data} ────────│
```

## 八、常见问题

### Q：Access Token 过期了怎么办？
用 Refresh Token 调 `/refresh/` 换一个新的 Access Token，无需重新登录。

### Q：刷新时 access 和 refresh 都回来是为什么？
因为 `ROTATE_REFRESH_TOKENS=True`，每次刷新会同时签发新的 access 和新的 refresh，旧的 refresh 立刻作废。

### Q：怎么让用户"退出登录"？
客户端删除本地存储的 token，同时服务端从 Redis 白名单中删除对应的 refresh token jti。即便 token 还没过期，刷新时也会被拒绝。Access token 在有效期内仍可使用，所以退出时两部分都要处理。

### Q：`refresh["jti"]` 是什么？
JWT ID，每条 token 的唯一标识，存储在 payload 里。用于白名单/黑名单的场景下精确追踪某个 token。
