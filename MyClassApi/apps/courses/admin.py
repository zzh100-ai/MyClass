from django.contrib import admin
from .models import Category, Course, Chapter, Lesson


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'sort_order']
    list_filter = ['parent']
    search_fields = ['name']


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0
    fields = ['title', 'sort_order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'teacher', 'price', 'is_free', 'status', 'learn_count', 'created_at']
    list_filter = ['status', 'is_free', 'category']
    search_fields = ['title', 'teacher__username']
    inlines = [ChapterInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['title', 'duration', 'is_preview', 'sort_order']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'sort_order']
    search_fields = ['title', 'course__title']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'duration', 'is_preview']
    list_filter = ['is_preview']
    search_fields = ['title', 'chapter__title']
