"""
课程搜索 API

使用 Elasticsearch + IK 分词器实现中文全文检索。
视图类结构已搭建好，核心查询逻辑以 TODO 标注，由用户完成。
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CourseSearchSerializer

# TODO: 导入 ES 客户端和 Redis 缓存
# from elasticsearch_dsl import Search
# from elasticsearch_dsl.query import MultiMatch, Bool, Term, Range, MatchAll
# from django.core.cache import caches
# from apps.search.documents import CourseDocument
# from apps.search.hotwords import HOTWORDS_KEY, HOTWORDS_TOP_N, HOTWORDS_MAX_SIZE

# ES搜索结果中每个文档映射的字段
SEARCH_RESULT_FIELDS = [
    'id', 'title', 'subtitle', 'description', 'cover_image',
    'category_id', 'category_name', 'teacher_name',
    'price', 'original_price', 'is_free', 'learn_count', 'status',
]


class SearchView(viewsets.ViewSet):
    """课程搜索视图"""

    @action(detail=False, methods=['get'])
    def courses(self, request):
        """
        GET /api/v1/search/courses/?q=关键词&category_id=1&...

        TODO: 实现 ES 全文搜索（核心逻辑）
        步骤:
        1. 用 CourseSearchSerializer 校验 query_params
        2. 构建 ES Search 对象: s = CourseDocument.search()
        3. 构建 MultiMatch query（对 title、subtitle、description 加权搜索）
        4. 构建 Bool query，合并关键词搜索 + 筛选条件（category、价格区间、免费）
        5. 设置分页: s = s[(page-1)*page_size : page*page_size]
        6. 设置高亮: s = s.highlight('title', 'description')
           → 高亮需要先从 ES Index 查询，参数需要用 .update() 传递 highlight 字典
        7. 执行查询: response = s.execute()
        8. 组装返回结果:
           {
               "total": response.hits.total.value,
               "results": [
                   {
                       "id": hit.meta.id,
                       "title": hit.title,
                       "highlight": { ...片段 },
                       ...
                   }
               ]
           }

        提示: IK 分词器在 ES mapping 中已配置好，Search DSL 会自动使用。
        """
        # 校验参数
        params = CourseSearchSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        q = params.validated_data['q']

        # TODO: 实现上述 7 个步骤的 ES 搜索逻辑
        # s = CourseDocument.search()
        # ... 你的代码 ...

        # 搜索成功后，记录热词
        # import hotwords; hotwords.record_hotword(q)  # TODO: 取消注释

        # 临时占位：返回空结果
        return Response({
            'q': q,
            'total': 0,
            'results': [],
        })

    @action(detail=False, methods=['get'])
    def hotwords(self, request):
        """
        GET /api/v1/search/hotwords/
        返回搜索热词排行榜

        TODO: 实现 Redis ZSET 热词查询
        步骤:
        1. 使用 ZREVRANGE 获取 HOTWORDS_TOP_N 个热词及分数
        2. 返回格式: [{"word": "Django", "count": 128}, ...]
        """
        # TODO: 实现热词查询
        return Response([])


# ===== 热词辅助函数（在 views 外部，由上面的 action 调用）=====

# TODO: 将下面两个函数移到 hotwords.py 中实现，然后在 views 中 import 使用
