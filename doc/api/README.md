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
