import os
from celery import Celery

# 设置 Django 默认配置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("myclass")

# 从 Django 配置中读取命名空间为 CELERY_ 的配置项
app.config_from_object("django.conf:settings", namespace="CELERY")

# 自动发现所有已注册 Django app 中的 tasks.py
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
