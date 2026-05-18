from django.db import models


class Category(models.Model):
    """课程分类模型（支持二级分类）"""

    name = models.CharField(max_length=100, verbose_name="分类名称")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="父分类"
    )
    sort_order = models.IntegerField(default=0, verbose_name="排序权重")

    class Meta:
        db_table = "course_categories"
        verbose_name = "课程分类"
        verbose_name_plural = verbose_name
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name
