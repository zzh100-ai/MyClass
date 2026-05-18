from rest_framework import viewsets
from apps.courses.models import Category
from apps.courses.serializers.category import CategorySerializer
from rest_framework.permissions import IsAdminUser


class CategoryViewSet(viewsets.ModelViewSet):
    """课程分类视图集（管理员管理）"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]  # 仅管理员可增删改查
