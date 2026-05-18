"""
Elasticsearch 课程文档定义

索引名: courses
分析器: IK 中文分词器（ik_max_word 用于索引，ik_smart 用于搜索）
"""

from elasticsearch_dsl import Document, Text, Float, Boolean, Integer, Date, Keyword, analyzer, connections

# IK 分词器：最大切分（索引时），智能切分（搜索时）
ik_max = analyzer('ik_max_word')
ik_smart = analyzer('ik_smart')


class CourseDocument(Document):
    """课程在 ES 中的文档映射"""

    # 全文检索字段
    title = Text(analyzer=ik_max, search_analyzer=ik_smart, fields={'keyword': Keyword()})
    subtitle = Text(analyzer=ik_max, search_analyzer=ik_smart)
    description = Text(analyzer=ik_max, search_analyzer=ik_smart)

    # 过滤/排序字段
    category_id = Integer()
    category_name = Keyword()
    teacher_id = Integer()
    teacher_name = Keyword()
    price = Float()
    is_free = Boolean()
    status = Keyword()
    learn_count = Integer()
    cover_image = Keyword(index=False)  # 不参与检索，仅存储

    # 嵌套章节（不参与检索，仅存储）
    chapters = Object(enabled=False)

    created_at = Date()
    updated_at = Date()

    class Index:
        name = 'courses'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    @classmethod
    def from_course(cls, course, chapters_data=None):
        """从 Django Course 模型构建 ES 文档"""
        doc = cls(
            meta={'id': course.id},
            title=course.title,
            subtitle=course.subtitle or '',
            description=course.description or '',
            category_id=course.category_id,
            category_name=course.category.name if course.category else '',
            teacher_id=course.teacher_id,
            teacher_name=course.teacher.username if course.teacher else '',
            price=float(course.price),
            is_free=course.is_free,
            status=course.status,
            learn_count=course.learn_count,
            cover_image=course.cover_image.url if course.cover_image else '',
            chapters=list(chapters_data) if chapters_data else [],
            created_at=course.created_at,
            updated_at=course.updated_at,
        )
        return doc
