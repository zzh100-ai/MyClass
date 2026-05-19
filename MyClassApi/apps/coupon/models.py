"""
优惠券数据模型

三层抽象:
  活动(Activity) → 优惠类型(Coupon) → 优惠公式(pricing.py)
"""

from django.db import models
from apps.users.models import User


class Coupon(models.Model):
    """
    优惠券模板

    TODO: 理解字段含义
    1. discount_type 百分之/固定金额的区别？
    2. min_amount 的作用是什么？防止什么漏洞？
    3. valid_from/valid_to 过期策略？定时任务 vs 运行时检查？
    """
    class DiscountType(models.TextChoices):
        PERCENT = 'percent', '百分比折扣'    # 如 8折 → discount_value=80
        FIXED = 'fixed', '固定金额减免'      # 如 减¥30 → discount_value=30

    code = models.CharField(max_length=32, unique=True, verbose_name='优惠券编码')
    name = models.CharField(max_length=100, verbose_name='优惠券名称')
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices, verbose_name='折扣类型')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='折扣值')
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='最低消费金额')
    valid_from = models.DateTimeField(verbose_name='生效时间')
    valid_to = models.DateTimeField(verbose_name='失效时间')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    total_count = models.IntegerField(default=0, verbose_name='发行总量')
    used_count = models.IntegerField(default=0, verbose_name='已使用数量')
    description = models.TextField(blank=True, default='', verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            import random, hashlib, time
            raw = f'{self.name}{time.time()}{random.random()}'
            self.code = hashlib.md5(raw.encode()).hexdigest()[:12].upper()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'coupons'
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name

    @property
    def remaining(self):
        return self.total_count - self.used_count


class UserCoupon(models.Model):
    """
    用户领取的优惠券

    TODO: 思考
    1. 为什么优惠券模板和用户优惠券要分两张表？
    2. status 是否冗余？能否通过 used_at IS NULL 来推断？
    """
    class Status(models.TextChoices):
        UNUSED = 'unused', '未使用'
        USED = 'used', '已使用'
        EXPIRED = 'expired', '已过期'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons', verbose_name='用户')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='user_coupons', verbose_name='优惠券')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UNUSED, verbose_name='状态')
    received_at = models.DateTimeField(auto_now_add=True, verbose_name='领取时间')
    used_at = models.DateTimeField(null=True, blank=True, verbose_name='使用时间')

    class Meta:
        db_table = 'user_coupons'
        verbose_name = '用户优惠券'
        verbose_name_plural = verbose_name


class PointsTransaction(models.Model):
    """
    积分流水记录

    TODO: 理解
    1. 为什么积分要记录流水而不是只更新余额字段？
    2. type 分类的作用是什么？（后续统计/审计需要哪些维度？）
    """
    class TransactionType(models.TextChoices):
        REGISTER = 'register', '注册赠送'
        PURCHASE = 'purchase', '购买获赠'
        REDEEM = 'redeem', '抵扣使用'
        REFUND = 'refund', '退款退回'
        EXPIRE = 'expire', '积分过期'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_transactions', verbose_name='用户')
    amount = models.IntegerField(verbose_name='积分变动（正为获取，负为消费）')
    balance = models.IntegerField(verbose_name='变动后余额')
    type = models.CharField(max_length=20, choices=TransactionType.choices, verbose_name='变动类型')
    description = models.CharField(max_length=200, blank=True, verbose_name='描述')
    order = models.ForeignKey('order.Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联订单')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'points_transactions'
        verbose_name = '积分流水'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
