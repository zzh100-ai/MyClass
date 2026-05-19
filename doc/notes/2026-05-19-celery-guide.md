# Celery 异步任务入门教程

## 1. 什么是 Celery？

Celery 是一个分布式任务队列，用来处理 Django 请求之外的"后台任务"。典型场景：

- **耗时的操作**：发送邮件、生成报表 — 不能让用户干等
- **延迟执行的操作**：下单 30 分钟后未支付自动取消
- **定时任务**：每天统计订单数据、清理过期数据

### 同步 vs 异步

```
同步（用户等待）：
  用户 → 创建订单 → 发邮件 → 返回响应（用户等了 3 秒）

异步（用户不等待）：
  用户 → 创建订单 → 把"发邮件"任务丢给 Celery → 立即返回（用户等 0.1 秒）
                               ↓
                        Celery Worker 后台慢慢处理
```

## 2. 三个核心角色

```
┌─────────────┐     ┌──────────┐     ┌─────────────┐
│   Django    │ ──→ │  Redis   │ ──→ │ Celery      │
│  (生产者)   │     │ (Broker) │     │ Worker      │
│  app.views  │ ←── │          │     │ (消费者)    │
│             │     │          │     │ tasks.py    │
└─────────────┘     └──────────┘     └──────┬──────┘
                                            ↓
                                     ┌──────────┐
                                     │  Redis   │
                                     │ (结果)   │
                                     └──────────┘
```

| 角色 | 说明 | 在这个项目里 |
|------|------|-------------|
| **Producer（生产者）** | 发出任务的代码 | `apps/order/views.py`（下单时调度超时取消） |
| **Broker（消息队列）** | 存放任务的地方，Worker 从这里取任务 | Redis db 1 |
| **Worker（消费者）** | 真正执行任务的进程 | `celery -A config worker` |
| **Result Backend** | 存储任务执行结果（可选） | Redis db 1 |

## 3. 项目中的 Celery 配置

### 3.1 Celery 应用 (`config/celery.py`)

```python
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("myclass")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

关键点：
- `namespace="CELERY"` — 所有 Celery 配置项以 `CELERY_` 开头
- `autodiscover_tasks()` — 自动查找所有已注册 app 下的 `tasks.py`

### 3.2 配置项 (`config/settings.py`)

```python
CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"     # Redis db 1 作为消息队列
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"  # 结果也存 Redis db 1
CELERY_ACCEPT_CONTENT = ["json"]                     # 任务序列化格式
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Shanghai"                    # 时区
CELERY_TASK_TIME_LIMIT = 30 * 60                     # 单个任务最多跑 30 分钟
```

### 3.3 `__init__.py` 的作用

```python
from .celery import app as celery_app
__all__ = ("celery_app",)
```

这行确保 Django 启动时加载 Celery 应用，否则 `@shared_task` 不会被注册。

## 4. 定义任务

### 4.1 第一个任务 (`apps/order/tasks.py`)

```python
from celery import shared_task

@shared_task
def cancel_expired_order(order_id):
    """取消超时未支付的订单"""
    from .models import Order
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return {"status": "not_found"}

    if order.status != Order.Status.PENDING:
        return {"status": "skipped", "reason": f"订单状态为{order.status}"}

    order.status = Order.Status.CANCELLED
    order.save(update_fields=["status"])
    return {"status": "cancelled", "order_id": order_id}
```

### 4.2 `@shared_task` 详解

```python
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def my_task(self, arg1, arg2):
    try:
        # 业务逻辑
        pass
    except SomeError as exc:
        # 自动重试，最多 3 次，每次间隔 60 秒
        raise self.retry(exc=exc)
```

| 参数 | 说明 |
|------|------|
| `bind=True` | 让任务的第一个参数变成 `self`，可调用 `self.retry()` |
| `max_retries` | 最大重试次数 |
| `default_retry_delay` | 重试间隔（秒） |
| `name` | 自定义任务名称，默认是函数路径 `apps.order.tasks.cancel_expired_order` |

### 4.3 任务的最佳实践

1. **任务要能幂等执行** — 同一个任务执行两次，结果一致
2. **不要在任务里 import 模块顶部** — 因为 Worker 进程和 Django 进程不同。在函数内部 import 或使用延迟导入
3. **参数尽量简单** — 传 ID 而不是传整个对象

```python
# ✅ 正确：传 ID，在任务内部查数据库
@shared_task
def send_notification(user_id):
    user = User.objects.get(id=user_id)
    ...

# ❌ 错误：传对象（可能被序列化问题坑）
@shared_task
def send_notification(user):
    ...
```

## 5. 调度任务

### 5.1 立即执行

```python
from .tasks import my_task

my_task.delay(arg1="hello", arg2="world")
```

### 5.2 延迟执行（最常用）

```python
# 30 秒后执行
my_task.apply_async(args=[order_id], countdown=30)

# 30 分钟后执行（本项目中的订单超时取消）
cancel_expired_order.apply_async(
    args=[order.id],
    countdown=ORDER_TIMEOUT,       # 30 * 60 = 1800 秒
    task_id=f"cancel_order_{order.id}"  # 自定义任务 ID，方便后续撤销
)
```

### 5.3 指定时间执行

```python
from datetime import datetime, timedelta
from celery import current_app

# 明天上午 10 点执行
eta = datetime.now() + timedelta(days=1)
eta = eta.replace(hour=10, minute=0, second=0)

my_task.apply_async(args=[id], eta=eta)
```

### 5.4 撤销任务

```python
# 用之前自定义的 task_id 撤销
from .tasks import cancel_expired_order
cancel_expired_order.AsyncResult(f"cancel_order_{order.id}").revoke()
```

注意：`revoke()` 只能撤销还在队列中的任务。如果 Worker 已经开始执行了，任务会继续执行完（除非加上 `terminate=True`，但不推荐）。

## 6. 运行 Worker

```bash
# 进入 Django 项目目录
cd MyClassApi

# 启动 Worker（前台运行，能看到日志）
celery -A config worker -l info

# 指定并发数（默认 CPU 核心数）
celery -A config worker -l info --concurrency=4

# Windows 上需要加 -P solo（否则可能启动失败）
celery -A config worker -l info -P solo
```

Worker 启动后，你会看到：

```
[tasks]
  . apps.order.tasks.cancel_expired_order
  . config.celery.debug_task
```

这说明任务已被自动发现和注册。

## 7. 实际流程演示

以本项目中的订单超时取消为例：

```
1. 用户下单
   OrderViewSet.create() 创建订单
                              ↓
2. 调度超时任务
   cancel_expired_order.apply_async(
       args=[order.id],
       countdown=1800,           ← 30 分钟
       task_id=f"cancel_order_{order.id}"
   )
                              ↓
3. 时间流逝 30 分钟...
   如果用户支付了 → 撤销任务，订单为 paid
   如果没支付     → Worker 执行 cancel_expired_order
                              ↓
4. 任务执行
   order.status = cancelled
   优惠券恢复为 unused
                              ↓
5. 用户看到订单状态：已取消
```

## 8. 定时任务（Periodic Tasks / Beat）

如果需要每天固定时间执行（比如凌晨统计），需要额外启动 Celery Beat。

### 8.1 安装 celery-beat

```bash
pip install celery[beat]  # 或者直接启动 beat
```

### 8.2 定义定时任务

在 `config/celery.py` 中添加：

```python
app.conf.beat_schedule = {
    "daily-order-statistics": {
        "task": "apps.order.tasks.daily_statistics",
        "schedule": crontab(hour=3, minute=0),  # 每天凌晨 3 点
    },
}
```

### 8.3 启动 Beat

```bash
# 同时启动 Worker 和 Beat
celery -A config worker -l info -B

# 或者分开启动（推荐）
celery -A config worker -l info       # 终端 1
celery -A config beat -l info          # 终端 2
```

## 9. 监控：Flower

Flower 是 Celery 的 Web 监控面板。

### 9.1 安装

```bash
pip install flower
```

### 9.2 启动

```bash
celery -A config flower --port=5555
```

打开 `http://localhost:5555` 可以看到：
- 哪些 Worker 在线
- 任务执行状态（成功/失败）
- 任务耗时统计
- 队列深度

## 10. 常见问题

### 10.1 Windows 上启动 Worker 报错

加 `-P solo` 参数：

```bash
celery -A config worker -l info -P solo
```

### 10.2 任务找不到（Received unregistered task of type ...）

- 确保 `config/__init__.py` 中有 `from .celery import app as celery_app`
- 确保 tasks.py 在 `INSTALLED_APPS` 的某个 app 目录下
- 检查 Worker 启动日志，确认任务名出现在 `[tasks]` 列表中

### 10.3 任务执行了但好像没效果

检查任务的返回值：

```python
result = my_task.delay(arg)
result.get(timeout=10)  # 获取执行结果（会阻塞，仅用于调试）
```

### 10.4 Redis 连接问题

```bash
redis-cli ping  # 应该返回 PONG
celery -A config inspect ping  # 检查 Worker 是否存活
```

### 10.5 本项目中的重要文件

| 文件 | 说明 |
|------|------|
| `config/celery.py` | Celery 应用定义 |
| `config/__init__.py` | 确保 Django 加载 Celery |
| `config/settings.py` | `CELERY_*` 配置项 |
| `apps/order/tasks.py` | 订单超时取消任务 |
| `apps/order/views.py` | 调度和撤销任务的地方 |

## 11. 快速开始（在本项目中）

```bash
# 终端 1：启动 Django
cd MyClassApi
python manage.py runserver

# 终端 2：启动 Celery Worker
cd MyClassApi
celery -A config worker -l info -P solo

# 终端 3（可选）：启动 Flower 监控
celery -A config flower --port=5555
```

下单后等 30 分钟（或临时把 `ORDER_TIMEOUT` 改成 30 秒测试），订单会自动取消。
