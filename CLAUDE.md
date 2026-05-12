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

- **配置文件：** `MyClassApi/settings.py` — 默认使用 SQLite 数据库，DEBUG=True，尚未安装 DRF 或其他外部应用。
- **URL 根路由：** `MyClassApi/urls.py` — 目前仅注册了 Django admin。
- **Django 项目名**为 `MyClassApi`。运行 `manage.py` 时，`DJANGO_SETTINGS_MODULE` 指向 `MyClassApi.settings`。

### 前端 — Vue 3（MyClassWeb/）

- **入口文件：** `src/main.js` — 创建 Vue 实例，安装 Pinia 和 Vue Router。
- **路由：** `src/router/index.js` — createWebHistory 模式，路由表为空。
- **状态管理：** Pinia store 文件放在 `src/stores/`，每个业务概念一个文件。
- **路径别名：** `@` 映射到 `src/`（在 `vite.config.js` 中配置）。

## 计划引入的技术栈（逐步引入）

以下技术将根据功能需求逐步引入：

- **DRF（Django REST Framework）：** 用于构建 REST API 端点、序列化器、视图集。
- **Redis + Celery：** 用于异步任务（邮件、视频处理）和缓存。
- **Elasticsearch：** 用于课程搜索。
- **MySQL：** 在需要持久化存储时替换 SQLite。

## 约定

- 后端 app 放在 `MyClassApi/` 下，作为 Django app（`python manage.py startapp <name>`）。
- 前端页面放在 `MyClassWeb/src/views/`，组件放在 `src/components/`。
- 前端通过环境变量（`VITE_API_BASE_URL`）配置 API 基础地址，禁止硬编码。
- 后端 API 路由统一使用 `/api/v1/` 命名空间。
- 所有共享的前端状态（用户认证、课程数据等）使用 Pinia store 管理。
- 语言：所有代码、注释、提交信息和文档使用中文。

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
