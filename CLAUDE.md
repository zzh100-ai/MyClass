# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在此仓库中工作时提供指引。

## 项目概览

MyClass 是一个前后端分离的在线教育平台。两个顶层目录是独立的项目，各自管理依赖——命令需要在各自的目录下执行，不能从仓库根目录运行。

| 目录 | 技术栈 | 说明 |
|-----------|-------|-------------|
| `MyClassApi/` | Django 4.2 + DRF | REST API 后端 |
| `MyClassWeb/` | Vue 3 + Vite + Pinia | SPA 前端 |

## 常用命令

### 后端（MyClassApi/）

```bash
cd MyClassApi
python manage.py runserver          # 启动开发服务器（http://localhost:8000）
python manage.py migrate            # 执行数据库迁移
python manage.py makemigrations     # 生成新的迁移文件
python manage.py createsuperuser    # 创建管理员账户
python manage.py shell              # Django 交互式 shell
python manage.py test               # 运行所有测试
python manage.py test app_name      # 运行指定 app 的测试
python manage.py test app_name.tests.test_file  # 运行指定的测试文件
```

### 前端（MyClassWeb/）

```bash
cd MyClassWeb
npm install          # 安装依赖
npm run dev          # 启动 Vite 开发服务器（热更新）
npm run build        # 生产构建
npm run preview      # 本地预览生产构建
```

## 架构

### 后端 — Django 4.2（MyClassApi/）

- **配置文件：** `config/settings.py` — MySQL 数据库、Redis 缓存、DRF + SimpleJWT 已集成。
- **路由：** `config/urls.py`，API 统一挂载在 `/api/v1/` 下。
  - `/api/v1/auth/` → `apps.users.urls`（注册、登录、token 刷新）
  - `/admin/` → Django admin
- **用户模型：** 自定义 `User`（继承 `AbstractUser`），`AUTH_USER_MODEL = "users.User"`，app 位于 `apps/users/`。
- 运行 `manage.py` 时，`DJANGO_SETTINGS_MODULE` 指向 `config.settings`。

### 前端 — Vue 3（MyClassWeb/）

- **入口文件：** `src/main.js` — 创建 Vue 实例，安装 Pinia 和 Vue Router。
- **路由：** `src/router/index.js` — createWebHistory 模式，路由表为空。
- **状态管理：** Pinia store 文件放在 `src/stores/`，每个业务概念一个文件。
- **路径别名：** `@` 映射到 `src/`（在 `vite.config.js` 中配置）。

## 技术栈状态

| 技术 | 状态 | 用途 |
|------|------|------|
| Django 4.2 | ✅ 已集成 | Web 框架 |
| DRF | ✅ 已集成 | REST API |
| SimpleJWT | ✅ 已集成 | JWT 登录认证 |
| MySQL 8.0 | ✅ 已集成 | 关系数据库 |
| Redis | ✅ 已集成 | 缓存（后续 Celery broker） |
| Celery | ⏳ 待引入 | 异步任务 |
| Elasticsearch | ⏳ 待引入 | 课程搜索 |

## 约定

- 后端 app 放在 `MyClassApi/` 下，作为 Django app（`python manage.py startapp <name>`）。
- 前端页面放在 `MyClassWeb/src/views/`，组件放在 `src/components/`。
- 前端通过环境变量（`VITE_API_BASE_URL`）配置 API 基础地址，禁止硬编码。
- 后端 API 路由统一使用 `/api/v1/` 命名空间。
- 所有共享的前端状态（用户认证、课程数据等）使用 Pinia store 管理。
- 语言：所有代码、注释、提交信息和文档使用中文。

## 开发协作模式

本项目采用"框架搭建 + TODO 标注"的教学开发模式：

1. **Claude 负责：** 搭建技术框架、配置基础设施、定义接口规范、创建文件结构
2. **用户负责：** 完成 TODO 标注的业务逻辑、字段验证、异常处理等核心代码

开发新功能时，Claude 先创建完整的框架代码，在需要用户自己实现的位置用 `# TODO: ...` 注释标注，格式如下：

```python
# TODO: 添加手机号格式验证（正则匹配中国大陆手机号 1[3-9]\d{9}）
# TODO: 添加密码强度验证（至少8位，包含字母和数字）
```

这些 TODO 是给用户的练习任务，帮助用户在实践中掌握各个技术栈。

## 文档维护

以下文档必须在开发过程中同步更新，不得滞后于代码：

| 变更场景 | 需更新的文档 |
|----------|-------------|
| 新增或修改 API 接口 | `doc/api/` 下对应模块的接口文档 |
| 搭建新模块 / 引入新技术 | `doc/tutorials/` 下对应的教程文档 |
| 遇到技术问题及解决方案 | `doc/notes/` 下按日期命名的笔记文件 |

- `doc/api/README.md` 作为 API 索引，每新增一个模块时追加接口摘要。
- `doc/tutorials/README.md` 作为教程目录，完成一个阶段的教程后更新进度。
- `doc/notes/README.md` 作为笔记索引，每新增一篇笔记时添加条目。
- 笔记文件命名格式：`YYYY-MM-DD-主题.md`（如 `2026-05-12-django-orm.md`）。
