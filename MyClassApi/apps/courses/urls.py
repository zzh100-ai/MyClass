from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ChapterViewSet, LessonViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
