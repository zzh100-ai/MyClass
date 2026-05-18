from rest_framework import serializers
from apps.courses.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """课程分类序列化器"""

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "sort_order"]
        read_only_fields = ["id"]
