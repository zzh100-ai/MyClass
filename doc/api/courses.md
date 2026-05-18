# 课程模块 API

## 课程管理

### 课程列表

```
GET /api/v1/courses/?category=<category_id>&page=<page>&page_size=<size>

Query Parameters:
- category: 分类ID（可选）
- page: 页码（默认1）
- page_size: 每页数量（默认20，最大100）

Response 200:
{
    "count": 100,
    "next": "http://localhost:8000/api/v1/courses/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Django 入门到精通",
            "subtitle": "从零搭建企业级应用",
            "description": "课程详情简介",
            "cover_image": "/media/covers/2026/05/django.jpg",
            "category": 2,
            "category_name": "后端开发",
            "teacher": 5,
            "teacher_name": "张三老师",
            "price": "199.00",
            "original_price": "299.00",
            "is_free": false,
            "points_required": null,
            "coupon_config": null,
            "status": "published",
            "learn_count": 128,
            "created_at": "2026-05-14T10:00:00Z",
            "updated_at": "2026-05-14T10:00:00Z"
        }
    ]
}
```

### 课程详情（含章节+课时）

```
GET /api/v1/courses/{id}/

Response 200:
{
    "id": 1,
    "title": "Django 入门到精通",
    "subtitle": "从零搭建企业级应用",
    "description": "课程详情简介",
    "cover_image": "/media/covers/2026/05/django.jpg",
    "category": 2,
    "category_name": "后端开发",
    "teacher": 5,
    "teacher_name": "张三老师",
    "price": "199.00",
    "original_price": "299.00",
    "is_free": false,
    "points_required": null,
    "coupon_config": null,
    "status": "published",
    "learn_count": 128,
    "created_at": "2026-05-14T10:00:00Z",
    "updated_at": "2026-05-14T10:00:00Z",
    "chapters": [
        {
            "id": 1,
            "title": "第一章 Django 基础",
            "summary": "介绍Django安装与配置",
            "sort_order": 0,
            "lessons": [
                {
                    "id": 1,
                    "title": "1.1 Django 安装",
                    "video_url": "https://example.com/video1.mp4",
                    "duration": 360,
                    "sort_order": 0,
                    "is_preview": true,
                    "created_at": "..."
                }
            ],
            "created_at": "..."
        }
    ]
}
```

### 创建课程（教师/管理员）

```
POST /api/v1/courses/
Authorization: Bearer <access_token>
Content-Type: application/json

Body:
{
    "title": "Vue3 实战",
    "subtitle": "从入门到项目上线",
    "description": "<p>课程详细介绍</p>",
    "cover_image": null,
    "category": 3,
    "price": 99.00,
    "original_price": 199.00,
    "is_free": false,
    "status": "draft"
}

Response 201: 同课程详情结构（不包含 chapters）
```

> ⚠️ **注意**：`teacher` 字段由后端**自动设为当前登录用户**，请求体中无需也不可传入。`cover_image` 为**可选字段**，传 `null` 或不传均可。

### 更新课程（教师/管理员）

```
PUT /api/v1/courses/{id}/
PATCH /api/v1/courses/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

Body（PUT 全量更新）:
{
    "title": "Vue3 实战",
    "subtitle": "从入门到项目上线",
    "description": "<p>课程详细介绍</p>",
    "cover_image": null,
    "category": 3,
    "price": 99.00,
    "original_price": 199.00,
    "is_free": false,
    "status": "published"
}

Body（PATCH 部分更新）:
{
    "status": "published"
}

Response 200: 更新后的课程对象
```

### 删除课程（教师/管理员）

```
DELETE /api/v1/courses/{id}/
Authorization: Bearer <access_token>

Response 204: 无内容
```

---

## 章节管理

### 创建章节

```
POST /api/v1/chapters/
Authorization: Bearer <access_token>

Body:
{
    "course": 1,
    "title": "第二章 Django 模型",
    "summary": "学习ORM和数据建模",
    "sort_order": 1
}

Response 201:
{
    "id": 2,
    "course": 1,
    "course_title": "Django 入门到精通",
    "title": "第二章 Django 模型",
    "summary": "学习ORM和数据建模",
    "sort_order": 1,
    "lessons_count": 0,
    "created_at": "..."
}
```

### 更新/删除章节

```
PUT /api/v1/chapters/{id}/   # 更新
DELETE /api/v1/chapters/{id}/ # 删除
```

---

## 课时管理

### 创建课时

```
POST /api/v1/lessons/
Authorization: Bearer <access_token>

Body:
{
    "chapter": 1,
    "title": "2.1 定义模型",
    "video_url": "https://example.com/lesson2_1.mp4",
    "duration": 540,
    "sort_order": 0,
    "is_preview": false
}

Response 201:
{
    "id": 2,
    "chapter": 1,
    "chapter_title": "第二章 Django 模型",
    "title": "2.1 定义模型",
    "video_url": "https://example.com/lesson2_1.mp4",
    "duration": 540,
    "sort_order": 0,
    "is_preview": false,
    "created_at": "..."
}
```

### 更新/删除课时

```
PUT /api/v1/lessons/{id}/   # 更新
DELETE /api/v1/lessons/{id}/ # 删除
```

---

## 分类管理（管理员）

### 分类列表（公开）

```
GET /api/v1/categories/

Response 200:
[
    {
        "id": 1,
        "name": "后端开发",
        "parent": null,
        "sort_order": 0
    },
    {
        "id": 2,
        "name": "Python",
        "parent": 1,
        "sort_order": 1
    }
]
```

### 创建/更新/删除分类（仅管理员）

```
POST   /api/v1/categories/   # 创建
PUT    /api/v1/categories/{id}/   # 更新
DELETE /api/v1/categories/{id}/   # 删除
```

---

## 字段说明

| 字段 | 类型 | 创建 | 更新 | 说明 |
|------|------|------|------|------|
| `title` | string | **必填** | 可改 | 课程标题 |
| `subtitle` | string | 可选 | 可改 | 副标题 |
| `description` | text | 可选 | 可改 | 课程详情 |
| `cover_image` | file | **可选** | 可改 | 封面图，可传 `null` 或不传 |
| `category` | integer | 可选 | 可改 | 分类 ID |
| `teacher` | integer | **只读** | 只读 | **后端自动赋值为当前用户** |
| `price` | decimal | **必填** | 可改 | 当前售价（≥ 0） |
| `original_price` | decimal | 可选 | 可改 | 原价（必须 ≥ `price`） |
| `is_free` | boolean | 可选 | 可改 | 免费课程；为 `true` 时 `price` 必须为 0 |
| `points_required` | integer | 预留 | 预留 | 积分兑换所需分数 |
| `coupon_config` | json | 预留 | 预留 | 优惠规则配置 |
| `status` | string | 可选 | 可改 | `draft` / `published` / `archived`，默认 `draft` |
| `learn_count` | integer | **只读** | 只读 | 学习人数，自动累加 |

## 业务规则

- **价格验证**：免费课程（`is_free=True`）的 `price` 必须为 0；若提供 `original_price`，必须 ≥ `price`
- **权限**：未登录用户可查看课程列表/详情；只有课程教师或管理员可创建/更新/删除课程及下属章节/课时
- **嵌套序列化**：课程详情接口自动返回完整的章节+课时树形结构
- **教师自动赋值**：`teacher` 字段由后端 `perform_create` 自动设为当前登录用户，客户端不可修改
