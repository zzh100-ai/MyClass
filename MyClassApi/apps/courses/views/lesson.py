from rest_framework import viewsets
from apps.courses.models import Lesson
from apps.courses.serializers.lesson import LessonSerializer
from apps.courses.permissions import IsTeacherOrReadOnly


class LessonViewSet(viewsets.ModelViewSet):
    """课时视图集"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrReadOnly]  # 教师可写，其他只读
