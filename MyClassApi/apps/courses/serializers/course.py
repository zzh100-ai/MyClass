from rest_framework import serializers
from apps.courses.models import Course
from .chapter import ChapterDetailSerializer


class CourseSerializer(serializers.ModelSerializer):
    """课程序列化器（列表/基础）"""
    category_name = serializers.CharField(source="category.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.username", read_only=True)
    teacher = serializers.PrimaryKeyRelatedField(read_only=True)  # 由后端自动设置
    cover_image = serializers.ImageField(required=False, allow_null=True)  # 允许空值

    class Meta:
        model = Course
        fields = [
            "id", "title", "subtitle", "description", "cover_image",
            "category", "category_name", "teacher", "teacher_name",
            "price", "original_price", "is_free", "points_required", "coupon_config",
            "status", "learn_count", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "learn_count", "created_at", "updated_at"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("价格不能为负数")
        return value

    def validate(self, attrs):
        # 免费课程价格必须为0
        if attrs.get('is_free') and attrs.get('price', 0) != 0:
            raise serializers.ValidationError({"price": "免费课程的价格必须为0"})
        # 原价必须大于等于当前售价（若原价存在）
        price = attrs.get('price', 0)
        original_price = attrs.get('original_price')
        if original_price is not None and original_price < price:
            raise serializers.ValidationError({"original_price": "原价不能低于当前售价"})
        return attrs


class CourseDetailSerializer(CourseSerializer):
    """课程详情序列化器（包含章节和课时）"""
    chapters = ChapterDetailSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ["chapters"]
