from rest_framework import viewsets
from apps.courses.models import Chapter
from apps.courses.serializers.chapter import ChapterSerializer
from apps.courses.permissions import IsTeacherOrReadOnly


class ChapterViewSet(viewsets.ModelViewSet):
    """章节视图集"""
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsTeacherOrReadOnly]  # 教师可写，其他只读
