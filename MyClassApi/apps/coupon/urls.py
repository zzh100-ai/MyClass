from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, UserCouponViewSet, PointsViewSet

router = DefaultRouter()
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'user-coupons', UserCouponViewSet, basename='user-coupon')
router.register(r'points', PointsViewSet, basename='points')

urlpatterns = [
    path('', include(router.urls)),
]
