# Django 项目搭建与配置

本文记录从零搭建 MyClassApi 后端项目的完整流程，涵盖项目结构规范化、MySQL 连接、Redis 缓存、DRF 集成以及环境变量管理。

---

## 1. 创建 Django 项目

```bash
conda activate luffycityapi
django-admin startproject MyClassApi
cd MyClassApi
```

## 2. 规范化项目结构

将 Django 自动生成的配置目录重命名，拆分出 `apps/` 存放业务应用：

```
MyClassApi/
├── apps/                  # 所有 Django app（业务模块）
│   └── __init__.py
├── config/                # Django 全局配置
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── requirements/          # 分环境依赖
│   └── base.txt
├── manage.py
└── .env                   # 敏感环境变量，不入 git
```

**关键变更：**
- 原先的 `MyClassApi/MyClassApi/` 重命名为 `MyClassApi/config/`
- 入口文件（`manage.py`、`wsgi.py`、`asgi.py`）中的 `DJANGO_SETTINGS_MODULE` 从 `MyClassApi.settings` 改为 `config.settings`
- `settings.py` 中的 `ROOT_URLCONF` 和 `WSGI_APPLICATION` 同步改为 `config.urls` / `config.wsgi.application`

## 3. 环境变量管理

使用 `python-dotenv` 加载 `.env` 文件，敏感信息不硬编码在 settings.py 中。

**.env 示例：**
```ini
SECRET_KEY=your-secret-key
DEBUG=True
MYSQL_DB=myclass
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
REDIS_URL=redis://127.0.0.1:6379/0
```

**settings.py 中读取方式：**
```python
from dotenv import load_dotenv
load_dotenv(BASE_DIR := Path(__file__).resolve().parent.parent / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True") == "True"
```

> `.env` 必须加入 `.gitignore`，防止敏感信息泄露。

## 4. 配置 MySQL

**创建数据库：**
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS myclass DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

**settings.py 配置：**
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DB", "myclass"),
        "USER": os.getenv("MYSQL_USER", "root"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", ""),
        "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

**依赖包：** `pip install mysqlclient`

> 如果安装 `mysqlclient` 失败（Windows 下常见），确保系统安装了 MySQL Connector C 或者换用 `PyMySQL` + `pymysql.install_as_MySQLdb()`。

## 5. 配置 Redis 缓存

**settings.py 配置：**
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
        },
    }
}
```

- `LOCATION` 中的 `/0` 表示使用 Redis 的第 0 号数据库
- `CONNECTION_POOL_KWARGS` 控制连接池上限，防止连接耗尽
- 后续配置 Celery 时，Broker 也会使用同一个 Redis 实例的不同 db 编号

## 6. 集成 DRF

在 `INSTALLED_APPS` 中添加：
```python
INSTALLED_APPS = [
    ...
    "rest_framework",
]
```

DRF 的核心能力（序列化器、视图集、路由器）将在创建第一个 API 时展开配置。

## 7. 其他配置调整

```python
LANGUAGE_CODE = "zh-hans"       # 中文界面
TIME_ZONE = "Asia/Shanghai"     # 上海时区
```

## 8. 验证

```bash
# 执行数据库迁移（验证 MySQL 连接）
python manage.py migrate

# 启动开发服务器（验证 Django 启动）
python manage.py runserver

# 访问 http://127.0.0.1:8000/admin/ — 应看到登录页面
```

---

## 下一步

- 创建第一个 Django app（如 `users` 用户模块）
- 编写用户模型（自定义 User 或扩展 Profile）
- 使用 DRF 暴露用户注册/登录 API
