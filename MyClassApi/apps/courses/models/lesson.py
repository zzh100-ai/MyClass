from django.db import models
from .chapter import Chapter


class Lesson(models.Model):
    """课程课时模型"""

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="lessons", verbose_name="所属章节")
    title = models.CharField(max_length=200, verbose_name="课时标题")
    video_url = models.CharField(max_length=500, blank=True, default="", verbose_name="视频地址")
    duration = models.IntegerField(default=0, verbose_name="视频时长（秒）")
    sort_order = models.IntegerField(default=0, verbose_name="排序")
    is_preview = models.BooleanField(default=False, verbose_name="是否可试看")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "course_lessons"
        verbose_name = "课时"
        verbose_name_plural = verbose_name
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"
