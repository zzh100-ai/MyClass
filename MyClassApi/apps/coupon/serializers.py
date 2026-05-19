from rest_framework import serializers
from .models import Coupon, UserCoupon, PointsTransaction


class CouponSerializer(serializers.ModelSerializer):
    """优惠券模板序列化器"""
    remaining = serializers.IntegerField(read_only=True)

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'name', 'discount_type', 'discount_value',
                  'min_amount', 'valid_from', 'valid_to', 'is_active',
                  'total_count', 'used_count', 'remaining', 'description']


class UserCouponSerializer(serializers.ModelSerializer):
    """用户优惠券序列化器"""
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = UserCoupon
        fields = ['id', 'coupon', 'status', 'received_at', 'used_at']


class CollectCouponSerializer(serializers.Serializer):
    """领取优惠券请求"""
    code = serializers.CharField(required=True, max_length=32,
                                 help_text='优惠券编码')

    # 添加校验
    def validate_code(self, value):
        # 1. 查找 coupon
        from .models import Coupon
        from django.utils.timezone import now
        try:
            coupon = Coupon.objects.first(code=value, is_active=True)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError('优惠券不存在或者已失效')
        # 2. 检查是否启用、是否在有效期
        if now() < coupon.valid_from or now() > coupon.valid_to:
            raise serializers.ValidationError('优惠券已过期')
        # 3. 检查是否已领完
        if coupon.used_count >= coupon.total_count:
            raise serializers.ValidationError('优惠券已领完')

        # 保存 coupon 到 context，collect 方法里需要它
        self.context['coupon'] = coupon
        return value


class PointsTransactionSerializer(serializers.ModelSerializer):
    """积分流水序列化器"""

    class Meta:
        model = PointsTransaction
        fields = ['id', 'amount', 'balance', 'type', 'description', 'created_at']
