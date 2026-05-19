"""
Django 配置文件

环境变量通过 .env 文件管理，使用 python-dotenv 加载。
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv(BASE_DIR := Path(__file__).resolve().parent.parent / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Application definition
INSTALLED_APPS = [
    "simpleui",  # 美化 Django admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 第三方
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    # 业务模块
    "apps.users.apps.UsersConfig",
    "apps.courses.apps.CoursesConfig",
    "apps.search.apps.SearchConfig",
    "apps.cart.apps.CartConfig",
    "apps.order.apps.OrderConfig",
    "apps.coupon.apps.CouponConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# 数据库 — MySQL
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

# Redis 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        "KEY_PREFIX": "",# 去掉前缀
        "VERSION": 0,  # 去掉版本号
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
        },
    },
    "courses": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("COURSES_REDIS_URL", "redis://127.0.0.1:6379/2"),
        "KEY_PREFIX": "",# 去掉前缀
        "VERSION": 0,  # 去掉版本号
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
        },
    },
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("COURSES_REDIS_URL", "redis://127.0.0.1:6379/2"),
        "KEY_PREFIX": "",  # 去掉前缀
        "VERSION": 0,  # 去掉版本号
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 自定义用户模型
AUTH_USER_MODEL = "users.User"

# DRF 全局配置
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# SimpleJWT 配置
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# CORS 跨域配置
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True

# 数据库查询日志（仅开发环境）
if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            # Django 的 SQL 记录器，输出所有数据库查询
            "django.db.backends": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
        },
    }


# -------------------- django-simpleui 配置 --------------------
SIMPLEUI_LOGO = "https://cdn.jsdelivr.net/npm/@simpleui/static@latest/logo.svg"
SIMPLEUI_HOME_TITLE = "MyClass 管理后台"
SIMPLEUI_HOME_ICON = "el-icon-s-platform"
SIMPLEUI_DEFAULT_THEME = "admin.lte.css"
SIMPLEUI_ANALYSIS = False

SIMPLEUI_CONFIG = {
    "system_keep": False,
    "menu_display": ["认证与授权", "用户管理", "课程管理", "优惠券管理", "订单管理"],
    "menus": [
        {"app": "users", "name": "认证与授权", "icon": "fas fa-shield-alt", "models": [
            {"name": "用户列表", "icon": "fas fa-user", "url": "/admin/users/user/"},
            {"name": "用户组", "icon": "fas fa-users", "url": "/admin/auth/group/"},
        ]},
        {"app": "courses", "name": "课程管理", "icon": "fas fa-book", "models": [
            {"name": "课程列表", "icon": "fas fa-video", "url": "/admin/courses/course/"},
            {"name": "课程分类", "icon": "fas fa-tags", "url": "/admin/courses/category/"},
            {"name": "章节管理", "icon": "fas fa-list", "url": "/admin/courses/chapter/"},
            {"name": "课时管理", "icon": "fas fa-play-circle", "url": "/admin/courses/lesson/"},
        ]},
        {"app": "coupon", "name": "优惠券管理", "icon": "fas fa-gift", "models": [
            {"name": "优惠券模板", "icon": "fas fa-ticket-alt", "url": "/admin/coupon/coupon/"},
            {"name": "用户优惠券", "icon": "fas fa-hand-holding-heart", "url": "/admin/coupon/usercoupon/"},
            {"name": "积分流水", "icon": "fas fa-coins", "url": "/admin/coupon/pointstransaction/"},
        ]},
        {"app": "order", "name": "订单管理", "icon": "fas fa-receipt", "url": "/admin/order/order/"}
    ],
}
