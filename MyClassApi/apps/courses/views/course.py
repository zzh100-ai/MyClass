from rest_framework import viewsets
from rest_framework.response import Response
from apps.courses.models import Course
from apps.courses.serializers.course import CourseSerializer, CourseDetailSerializer
from apps.courses.permissions import IsTeacherOrReadOnly

# 导入缓存模块（取消注释后使用）
from django.core.cache import caches
from utils.cache import CACHE_KEY_COURSE_LIST, CACHE_KEY_COURSE_DETAIL, CACHE_TTL_LIST, CACHE_TTL_DETAIL, \
    COURSE_CACHE_ALIAS

# coursers缓存
course_cache = caches[COURSE_CACHE_ALIAS]


class CourseViewSet(viewsets.ModelViewSet):
    """课程视图集"""
    queryset = Course.objects.all()
    permission_classes = [IsTeacherOrReadOnly]  # 教师可写，其他只读

    def get_serializer_class(self):
        # 详情接口使用嵌套序列化器，列表接口使用基础序列化器
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs

    def list(self, request, *args, **kwargs):
        """
        获取课程列表（带分类筛选）
        """
        # 生成缓存键
        category = request.query_params.get('category', "all")
        cache_key = CACHE_KEY_COURSE_LIST.format(category=category)

        # 尝试从redis中读取
        cache_data = course_cache.get(cache_key)
        if cache_data is not None:
            return Response(cache_data)

        # 没有命中 -> 查数据库
        response = super().list(request, *args, **kwargs)

        # 写入 Redis，15 分钟后过期
        course_cache.set(cache_key, response.data, CACHE_TTL_LIST)
        return response

    def retrieve(self, request, *args, **kwargs):
        """
        获取课程详情（含章节+课时嵌套）
        实现 Redis 缓存
          1. 从 kwargs 中获取 course_id
          2. 生成课程详情缓存键
          3. 缓存逻辑同 list（使用 CACHE_TTL_DETAIL 更长的过期时间）
        """
        # 获取 course_id
        course_id = kwargs.get('pk')
        cache_key = CACHE_KEY_COURSE_DETAIL.format(course_id=course_id)

        cache_data = course_cache.get(cache_key)
        if cache_data is not None:
            return Response(cache_data)
        response = super().retrieve(request, *args, **kwargs)
        course_cache.set(cache_key, response.data, CACHE_TTL_DETAIL)
        return response

    def perform_create(self, serializer):
        # 自动将当前用户设为课程的教师
        serializer.save(teacher=self.request.user)
        # 创建课程后，课程列表缓存已失效，需要清除
        course_cache.delete_pattern("courses:list:*")

    def perform_update(self, serializer):
        serializer.save()
        # 更新课程后，对应的列表缓存和该课程详情缓存都需要清除
        course_cache.delete_pattern("courses:list:*")
        course_cache.delete(
            CACHE_KEY_COURSE_DETAIL.format(course_id=serializer.instance.id)
        )


    def perform_destroy(self, instance):
        # 删除课程前，先记录该课程 ID，用于后续清除缓存
        course_id = instance.id
        instance.delete()
        # 删除课程后，清除列表缓存和该课程详情缓存
        course_cache.delete_pattern("courses:list:*")
        course_cache.delete(CACHE_KEY_COURSE_DETAIL.format(course_id=course_id))
