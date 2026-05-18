from django.db import models
from .course import Course


class Chapter(models.Model):
    """课程章节模型"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters", verbose_name="所属课程")
    title = models.CharField(max_length=200, verbose_name="章节标题")
    summary = models.TextField(blank=True, default="", verbose_name="章节简介")
    sort_order = models.IntegerField(default=0, verbose_name="排序")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "course_chapters"
        verbose_name = "章节"
        verbose_name_plural = verbose_name
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"
