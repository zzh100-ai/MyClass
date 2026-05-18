from rest_framework import serializers
from apps.courses.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    """课时序列化器（基础）"""
    chapter_title = serializers.CharField(source="chapter.title", read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "chapter", "chapter_title", "title", "video_url", "duration", "sort_order", "is_preview", "created_at"]
        read_only_fields = ["id", "created_at"]
