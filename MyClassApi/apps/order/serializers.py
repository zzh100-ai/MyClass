from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """订单明细序列化器"""

    class Meta:
        model = OrderItem
        fields = ['id', 'course', 'course_title', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_no', 'total_amount', 'final_amount',
                  'coupon_discount', 'points_discount', 'points_used',
                  'status', 'items', 'created_at', 'paid_at']
        read_only_fields = ['id', 'order_no', 'total_amount', 'status', 'created_at', 'paid_at']


class CreateOrderSerializer(serializers.Serializer):
    """
    创建订单请求

    添加字段校验
    1. course_ids 不能为空
    2. 每个 course_id 对应的课程必须存在
    3. 不能重复下单
    """
    course_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=True,
        min_length=1,
        help_text='课程ID列表（从购物车结算）'
    )

    # 添加购物车验证
    def validate_course_ids(self, value):
        from apps.courses.models import Course
        # 去重
        unique_ids = list(set(value))
        courses = Course.objects.filter(id__in=unique_ids, status='published')

        if len(courses) != len(value):
            found = {c.id for c in courses}
            missing = set(unique_ids) - found
            raise serializers.ValidationError(f'课程不存在或未发布: {missing}')
        user = self.context['request'].user
        # 检查是否有相同课程的待支付订单（防止重复点击）
        pending_order_ids = Order.objects.filter(
            user=user, status=Order.Status.PENDING
        ).values_list('id', flat=True)
        if pending_order_ids:
            existing = OrderItem.objects.filter(
                order_id__in=pending_order_ids,
                course_id__in=unique_ids
            )
            if existing.exists():
                raise serializers.ValidationError("你有相同课程的待支付订单，请先完成支付或取消")
        # 检查是否已购买（防止重复购买）
        paid_order_ids = Order.objects.filter(
            user=user, status=Order.Status.PAID
        ).values_list('id', flat=True)
        if paid_order_ids:
            bought = OrderItem.objects.filter(
                order_id__in=paid_order_ids, course_id__in=unique_ids
            ).values_list('course_id', flat=True)
            if bought:
                bought_titles = Course.objects.filter(id__in=bought).values_list('title', flat=True)
                raise serializers.ValidationError(f'已购买过: {", ".join(bought_titles)}')

        # 保存到context供view使用
        self.context["validated_courses"] = courses
        return unique_ids
