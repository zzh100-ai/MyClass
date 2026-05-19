"""
优惠券 + 积分 API
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Coupon, UserCoupon, PointsTransaction
from .serializers import (
    CouponSerializer, UserCouponSerializer,
    CollectCouponSerializer, PointsTransactionSerializer
)
from django.utils.timezone import now


# ==================== 优惠券模板管理（仅管理员）====================

class CouponViewSet(viewsets.ModelViewSet):
    """优惠券模板 CRUD（管理员）"""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]


# ==================== 用户优惠券 ====================

class UserCouponViewSet(viewsets.ReadOnlyModelViewSet):
    """用户优惠券列表"""
    serializer_class = UserCouponSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCoupon.objects.filter(user=self.request.user).select_related('coupon')

    @action(detail=False, methods=['post'])
    def collect(self, request):
        """
        POST /api/v1/user-coupons/collect/
        领取优惠券

        Body: {"code": "NEWUSER50"}

        实现领取逻辑
        1. 根据 code 查找 coupon
        2. 校验 coupon 是否启用、是否在有效期
        3. 校验剩余数量
        4. 检查是否已领取（同一券码每人只能领一次）
        5. 创建 UserCoupon 记录
        6. 增加 coupon.used_count（这里 used_count 是已领取数）
        7. 返回用户优惠券
        """
        serializer = CollectCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon = serializer.context['coupon']

        # 检查用户是否已经领取
        if UserCoupon.objects.filter(user=request.user, coupon=coupon).exists():
            return Response({'msg': '您已领取过该优惠券'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建
        user_coupon = UserCoupon.objects.create(user=request.user, coupon=coupon)
        coupon.used_count += 1
        coupon.save(update_fields=["used_count"])

        return Response(UserCouponSerializer(user_coupon).data, status=status.HTTP_201_CREATED)


# ==================== 积分 ====================

class PointsViewSet(viewsets.ViewSet):
    """积分管理"""
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/v1/points/
        当前积分余额

        实现
        1. 返回当前用户积分余额
        """
        return Response({'points': request.user.points})

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        GET /api/v1/points/history/
        积分流水记录
        """
        transactions = PointsTransaction.objects.filter(user=request.user)
        # 分页处理
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size

        total = transactions.count()
        items = transactions[start:end]

        return Response({
            'total': total,
            'results': PointsTransactionSerializer(items, many=True).data,
        })
