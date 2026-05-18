from django.db import models
from apps.users.models import User
from .category import Category


class Course(models.Model):
    """课程模型"""

    class Status(models.TextChoices):
        DRAFT = "draft", "草稿"
        PUBLISHED = "published", "已发布"
        ARCHIVED = "archived", "已归档"

    title = models.CharField(max_length=200, verbose_name="课程标题")
    subtitle = models.CharField(max_length=500, blank=True, default="", verbose_name="副标题")
    description = models.TextField(blank=True,null=True, default="", verbose_name="课程详情")
    cover_image = models.ImageField(upload_to="covers/%Y/%m/", blank=True, default="", verbose_name="封面图")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="courses", verbose_name="分类")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taught_courses", verbose_name="授课教师")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="当前售价")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="原价")
    is_free = models.BooleanField(default=False, verbose_name="是否免费")
    points_required = models.IntegerField(null=True, blank=True, verbose_name="积分兑换所需分数")
    coupon_config = models.JSONField(null=True, blank=True, verbose_name="优惠规则配置")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="课程状态"
    )
    learn_count = models.IntegerField(default=0, verbose_name="学习人数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "courses"
        verbose_name = "课程"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
