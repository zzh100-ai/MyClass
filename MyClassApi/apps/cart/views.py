"""
购物车 API

基于 Redis Hash 实现，支持高并发原子操作。
认证要求：所有接口均需要登录（购物车绑定用户）。
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CartAddSerializer
from apps.courses.models import Course

# 导入 Redis 和购物车工具函数
from django.core.cache import caches
from .redis_cart import add_course, remove_course, list_courses, clear_cart, get_cart_count


class CartViewSet(viewsets.ViewSet):
    """购物车视图集"""
    permission_classes = [IsAuthenticated]  # 所有操作需要登录

    def _get_redis(self):
        """获取 Redis 客户端（使用 cart 缓存）"""
        return caches['cart'].client.get_client()

    def list(self, request):
        """
        GET /api/v1/cart/
        获取购物车列表（含课程详情）
        1. carts = list_courses(redis, request.user.id) → [3, 5, 7]
        2. 根据 course_id 一次性从数据库查询课程详情
           courses = Course.objects.filter(id__in=carts)
        3. 组装数据返回
        """
        redis = self._get_redis()
        cart_ids = list_courses(redis, request.user.id)
        if not cart_ids:
            return Response([])

        # 实现购物车列表查询..
        from django.db.models import Case, When, Value, IntegerField

        preserved = Case(*[When(pk=pk, then=Value(i)) for i, pk in enumerate(cart_ids)], output_field=IntegerField())
        courses = Course.objects.filter(id__in=cart_ids).annotate(sort_order=preserved).order_by('sort_order')
        return Response([{
            'id': c.id,
            'title': c.title,
            'cover_image': c.cover_image.url if c.cover_image else '',
            'price': str(c.price),
            'is_free': c.is_free,
            'teacher_name': c.teacher.username if c.teacher else '',
        } for c in courses])

    def create(self, request):
        """
        POST /api/v1/cart/
        添加课程到购物车

        Body: {"course_id": 1}
        """
        redis = self._get_redis()
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = serializer.validated_data['course_id']

        # 调用 add_course(redis, request.user.id, course_id)
        #       返回 {"msg": "已添加到购物车"}
        #       如果课程已在购物车中，返回 {"msg": "课程已在购物车中"}
        added = add_course(redis, request.user.id, course_id)
        if not added:
            return Response({'msg': '课程已在购物车中'}, status=status.HTTP_200_OK)
        return Response({'msg': '已添加到购物车'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        DELETE /api/v1/cart/{course_id}/
        从购物车移除指定课程
        """
        redis = self._get_redis()

        # 调用 remove_course(redis, request.user.id, int(pk))
        #       返回 204 或 404（课程不在购物车中）
        success = remove_course(redis, request.user.id, int(pk))
        if not success:
            return Response({'msg': '课程不在购物车中'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """
        DELETE /api/v1/cart/clear/
        清空购物车
        """
        redis = self._get_redis()
        # 调用 clear_cart(redis, request.user.id)
        clear_cart(redis, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def count(self, request):
        """
        GET /api/v1/cart/count/
        获取购物车中课程数量
        """
        redis = self._get_redis()
        # 调用 get_cart_count(redis, request.user.id)
        count = get_cart_count(redis, request.user.id)
        return Response({'count': count})
