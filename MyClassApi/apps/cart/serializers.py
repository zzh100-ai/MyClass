from rest_framework import serializers
from apps.courses.models import Course


class CartAddSerializer(serializers.Serializer):
    """添加课程到购物车"""
    course_id = serializers.IntegerField(required=True, min_value=1)

    def validate_course_id(self, value):
        # 添加课程存在性验证
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("课程不存在")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    """购物车中单门课程的信息"""
    added_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "cover_image", "price", "is_free", "teacher_name", "added_at"]
