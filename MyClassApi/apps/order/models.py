from django.db import models
from apps.users.models import User
from apps.courses.models import Course


def generate_order_no():
    """
    生成唯一订单号
    格式: 20260518120000123456（日期+随机数）
    """
    import random
    from datetime import datetime
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    rand = str(random.randint(100000, 999999))
    return f'{ts}{rand}'


class Order(models.Model):
    """订单模型"""

    class Status(models.TextChoices):
        PENDING = 'pending', '待支付'
        PAID = 'paid', '已支付'
        CANCELLED = 'cancelled', '已取消'
        REFUNDED = 'refunded', '已退款'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    order_no = models.CharField(max_length=64, unique=True, default=generate_order_no, verbose_name='订单号')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='原订单金额')
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='实付金额')
    # 优惠券
    user_coupon = models.ForeignKey('coupon.UserCoupon', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='使用的优惠券')
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='优惠券减免')
    # 积分
    points_used = models.IntegerField(default=0, verbose_name='使用的积分')
    points_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='积分抵扣金额')

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name='订单状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order_no} - {self.user.username}'


class OrderItem(models.Model):
    """订单明细（记录购买时的课程快照）"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='所属订单')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name='课程')
    course_title = models.CharField(max_length=200, verbose_name='课程标题（快照）')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='购买时价格')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'order_items'
        verbose_name = '订单明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.order.order_no} - {self.course_title}'
