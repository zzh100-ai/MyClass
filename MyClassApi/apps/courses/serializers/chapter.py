from rest_framework import serializers
from apps.courses.models import Chapter
from .lesson import LessonSerializer


class ChapterDetailSerializer(serializers.ModelSerializer):
    """章节详情序列化器（包含课时列表）"""
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ["id", "title", "summary", "sort_order", "lessons", "created_at"]


class ChapterSerializer(serializers.ModelSerializer):
    """章节序列化器（列表/基础）"""
    course_title = serializers.CharField(source="course.title", read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ["id", "course", "course_title", "title", "summary", "sort_order", "lessons_count", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
