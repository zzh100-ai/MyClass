from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/courses/", include("apps.courses.urls")),
    path("api/v1/", include("apps.search.urls")),
    path("api/v1/", include("apps.cart.urls")),
    path("api/v1/", include("apps.order.urls")),
    path("api/v1/", include("apps.coupon.urls")),
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

