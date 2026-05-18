# 研究发现与技术要点

## 已确认的技术方案
- 课程模块采用基础 CRUD + 预留扩展字段
- 章节/课时使用标准树形结构（Course → Chapter → Lesson）
- 图片存储本地 media 目录（开发环境）

## 待学习/确认的技术点
- Redis Hash 操作命令（HSET, HGET, HDEL, HINCRBY）
- Elasticsearch 索引 mapping 设计
- Celery 异步任务定义与调用
- JWT Refresh Token 与黑名单机制
- DRF 权限类自定义
- Vue 3 组合式 API + Pinia 状态管理

## 踩坑记录（待补充）
- ...

## 参考资料
- Django ORM 官方文档
- DRF 文档 - 视图集与路由器
- Redis 文档 - 哈希类型
- Elasticsearch 中文分词配置
