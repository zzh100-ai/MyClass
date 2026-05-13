# Django 认证模块开发教程

本文记录用户认证模块（注册 + JWT 登录 + Token 刷新 + 失败限制）的完整开发流程。

---

## 1. 自定义用户模型

**关键决策：** 继承 `AbstractUser` 而非默认 `User`，方便后续扩展字段。

```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name="手机号")
```

**注意：** 必须在第一次 migrate 之前完成，否则需要重建数据库。

## 2. App 注册路径

app 放在 `apps/users/`，对应的模块路径是 `apps.users`：

```python
# apps/users/apps.py
class UsersConfig(AppConfig):
    name = "apps.users"  # 必须与 Python 模块路径一致
```

**settings.py 中的注册方式：**
```python
INSTALLED_APPS = [
    ...
    "apps.users.apps.UsersConfig",
]
AUTH_USER_MODEL = "users.User"  # app_label 是 name 的最后一段
```

## 3. SimpleJWT 配置

```python
# config/settings.py
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,           # 刷新时轮换 token
    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

## 4. 序列化器

- `RegisterSerializer` — 字段验证（手机号正则、密码强度、确认密码）+ `create()` 密码加密
- `LoginSerializer` — 多字段登录（用户名/手机号/邮箱），内部用 `Q` 查询 + `check_password` 校验
- `UserInfoSerializer` — 安全字段子集，统一视图返回格式

## 5. 视图

| 视图 | 功能 |
|------|------|
| `RegisterView` | 验证 → 创建用户 → 签发 JWT → 存入 Redis 白名单 |
| `LoginView` | 验证凭据 → 签发 JWT → 存入 Redis 白名单 |
| `CustomTokenRefreshView` | 验证旧 token 在白名单 → 删旧存新 → 签发新 token |

## 6. Refresh Token Redis 白名单

**原理：** 签发时写 Redis，刷新时验证 → 删旧 → 写新，退出时删除（待开发）。

```python
def store_refresh_token(refresh, user):
    conn = get_redis_connection("default")
    conn.set(f"refresh_token:{refresh['jti']}", user.id, ex=3600 * 24 * 7)
```

刷新时的关键逻辑：
1. 解码旧的 refresh token，用 `jti` 查 Redis 是否存在
2. 不在白名单 → 返回 401（token 已失效或被重复使用）
3. 在白名单 → 删除旧记录，调用父类签发新 token，存入新记录

## 7. 登录失败次数限制

**原理：** Redis 计数器 `login_fail:{identifier}`，每次失败 +1，5 次封禁 15 分钟。

```python
conn = get_redis_connection("default")
fail_key = f"login_fail:{identifier}"
fail_count = int(conn.get(fail_key) or 0)

if fail_count >= 5:
    raise serializers.ValidationError("登录失败次数过多")

new_count = conn.incr(fail_key)      # 原子递增
if new_count == 1:
    conn.expire(fail_key, 900)       # 首次设置过期时间
```

**关键坑：** `conn.get()` 返回 bytes，需要用 `int()` 转换。`conn.incr()` 返回 int，是原子操作更安全。

---

## 下一步

- 开发退出登录（DELETE Redis 白名单记录）
- 前端登录/注册页面
- 配置 CORS 跨域
