"""
订单与模拟支付 API

流程: 购物车 → 创建订单 → 支付 → 支付回调 → 订单状态变更

理解整个订单流转过程
  1. 创建订单时为什么要从购物车结算？为什么不直接下单？
  2. 支付回调的作用是什么？为什么支付结果要经由后端回调确认而非前端直接修改？
  3. 如果支付后没有收到回调（网络超时），如何保证订单状态最终一致？
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from apps.courses.models import Course
from apps.cart.redis_cart import remove_course
from django.utils.timezone import now
from django.core.cache import caches
from ..coupon.models import UserCoupon, PointsTransaction
from apps.coupon.pricing import calculate_final_price, POINTS_RATIO


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    订单视图集（只读：用户只能查看订单，不能修改）
    理解为什么继承 ReadOnlyModelViewSet
    而不是 ModelViewSet？订单的增删改查受什么限制？
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 用户只能查看自己的订单
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

    # ==================== 创建订单（特殊接口）====================

    def create(self, request):
        """
        POST /api/v1/orders/
        从购物车中创建订单

        实现创建订单的逻辑
        1. 校验参数（课程ID列表）
        2. 查询课程，计算总价
           courses = Course.objects.filter(id__in=course_ids, status='published')
           注意排除免费课程（总价只累加付费课程）
        3. 创建 Order 记录
           order = Order.objects.create(user=request.user, total_amount=total_price)
        4. 为每门课程创建 OrderItem（保存价格快照）
           OrderItem.objects.create(order=order, course=c, course_title=c.title, price=c.price)
        5. 清空购物车中这些课程（从 Redis 删除）
        6. 返回订单
        """
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        course_ids = serializer.validated_data['course_ids']
        user_coupon_id = request.data.get('coupon_id')
        points_to_use = int(request.data.get('points', 0))

        # 查询课程，计算总价
        courses = serializer.context['validated_courses']
        if len(courses) != len(course_ids):
            return Response({'msg': '部分课程不存在或未发布'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(c.price for c in courses if not c.is_free)

        # 查询优惠劵
        user_coupon = None
        if user_coupon_id:
            user_coupon = UserCoupon.objects.filter(
                id=user_coupon_id, user=request.user, status='unused'
            ).select_related('coupon').first()

        # 定价引擎计算
        price_result = calculate_final_price(total_amount, user_coupon, points_to_use)

        # 积分校验
        if price_result["points_discount"] > 0:
            points_cost = int(price_result["points_discount"] / POINTS_RATIO)
            if request.user.points < points_cost:
                return Response({'msg': '积分不足'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建订单
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            final_amount=price_result['final_price'],
            coupon_discount=price_result['coupon_discount'],
            points_discount=price_result['points_discount'],
            points_used=points_to_use,
            user_coupon=user_coupon)

        # 创建订单明细快照
        items = []
        for course in courses:
            items.append(OrderItem(
                order=order,
                course=course,
                course_title=course.title,
                price=course.price,
            ))
        OrderItem.objects.bulk_create(items)

        # 从购物车移除已购买的课程

        cart_redis = caches['cart'].client.get_client()
        for cid in course_ids:
            remove_course(cart_redis, request.user.id, cid)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # ==================== 模拟支付 ====================

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """
        POST /api/v1/orders/{id}/pay/
        模拟支付

        实现模拟支付
        1. 获取订单 order = self.get_object()
        2. 校验只有 pending 状态的订单可以支付
        3. 模拟支付处理（sleep 1秒模拟网络延迟）
        4. 调用 _handle_payment_success(order) 处理支付成功
        5. 返回支付成功信息
        """
        order = self.get_object()

        if order.status != Order.Status.PENDING:
            return Response({'msg': '订单状态不允许支付'}, status=status.HTTP_400_BAD_REQUEST)

        # 模拟支付延迟
        import time
        time.sleep(1)

        _handle_payment_success(order)
        return Response({'msg': '支付成功', 'order_no': order.order_no})

    # ==================== 支付回调 ====================

    @action(detail=False, methods=['post'])
    def notify(self, request):
        """
        POST /api/v1/orders/notify/
        模拟支付回调


        支付回调由支付平台（支付宝/微信）主动调用后端接口，
        通知订单支付结果。这里用模拟替代。

        Body:
        {
            "order_no": "20260518120000123456",
            "status": "paid"   # 模拟成功
        }

        实现支付回调处理
        1. 根据 order_no 查找订单
        2. 校验签名（模拟可跳过）
        3. 调用 _handle_payment_success(order)
        4. 返回成功响应（支付平台要求必须返回 success，否则会重复回调）
        """
        order_no = request.data.get('order_no')
        pay_status = request.data.get('status')

        try:
            order = Order.objects.get(order_no=order_no)
        except Order.DoesNotExist:
            return Response({'msg': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

        if pay_status == 'paid' and order.status == Order.Status.PENDING:
            _handle_payment_success(order)

        return Response({'msg': 'success'})


# ==================== 支付成功处理 ====================

def _handle_payment_success(order):
    """
    支付成功后的统一处理

    无论是 pay 接口还是 notify 回调，
    支付成功后都调用此函数处理。

    实现以下逻辑
    1. 修改订单状态为 paid
    2. 记录支付时间
    3. 为每门课程创建学习记录（Enrollment，后续完善）
    4. 从购物车移除已购买的课程
    5. 发送通知（邮件/站内信，后续 Celery 实现）
    """

    order.status = Order.Status.PAID
    order.paid_at = now()
    order.save()

    # 从购物车移除已购买的课程
    cart_redis = caches['cart'].client.get_client()
    for item in order.items.all():
        if item.course_id:
            from apps.cart.redis_cart import remove_course
            remove_course(cart_redis, order.user_id, item.course_id)

    # 扣减积分
    if order.points_used > 0:
        order.user.points -= order.points_used
        order.user.save(update_fields=['points'])
        PointsTransaction.objects.create(
            user=order.user, amount=-order.points_used, balance=order.user.points,
            type=PointsTransaction.TransactionType.REDEEM,
            description=f'订单{order.order_no}积分抵扣', order=order,
        )

    # 标记优惠券已使用
    if order.user_coupon:
        order.user_coupon.status = UserCoupon.Status.USED
        order.user_coupon.used_at = now()
        order.user_coupon.save(update_fields=['status', 'used_at'])
