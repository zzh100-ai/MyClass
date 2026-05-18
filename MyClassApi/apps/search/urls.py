from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SearchView

router = DefaultRouter()
router.register(r'search', SearchView, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]
