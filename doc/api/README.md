# API 文档

## 约定

- 基础路径：`http://localhost:8000/api/v1/`
- 数据格式：JSON
- 认证方式：待定（后续开发时确认 JWT 或 Session 方案）

## 接口列表

> 暂无 API 接口。创建第一个 Django app 后开始记录。

### 示例格式

| 方法 | 路径 | 说明 | 请求参数 | 响应 |
|------|------|------|----------|------|
| GET | `/api/v1/users/` | 用户列表 | `?page=1` | `{count, results: [...]}` |
| POST | `/api/v1/users/` | 注册用户 | `{username, password, email}` | `{id, username, email}` |

> 每新增一个模块的 API，在此文件中追加接口摘要，并在 `doc/api/` 下新建模块专属的 md 文件（如 `users.md`、`courses.md`）记录详细的请求/响应示例。
