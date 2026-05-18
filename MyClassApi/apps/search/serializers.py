from rest_framework import serializers


class CourseSearchSerializer(serializers.Serializer):
    """搜索请求参数"""
    q = serializers.CharField(required=True, min_length=1, max_length=100, help_text="搜索关键词")
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=10, min_value=1, max_value=50)
    # 可选的筛选条件
    category_id = serializers.IntegerField(required=False)
    price_min = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    price_max = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    is_free = serializers.BooleanField(required=False)
    ordering = serializers.ChoiceField(
        required=False,
        default='_score',
        choices=['_score', 'price_asc', 'price_desc', 'learn_count', 'newest'],
    )
