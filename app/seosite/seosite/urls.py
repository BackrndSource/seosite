from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.authtoken.views import obtain_auth_token

from django.contrib.sitemaps.views import index

from shop.urls import router as shop_router
from shop.urls import urlpatterns as shop_urlpatterns
from shop.urls import sitemaps as shop_sitemaps
from shop.views import robots_txt

sitemaps = {}
[sitemaps.setdefault(key, value) for key, value in shop_sitemaps.items()]

urlpatterns = (
    [
        # Admin
        path("admin/", admin.site.urls),
        # REST API
        path("api/", include((shop_router.urls, "shop"))),
        path("api/auth/", obtain_auth_token),
        # Sitemap.xml
        path("sitemap.xml", index, {"sitemaps": sitemaps}, name="sitemap"),
        # Robots.txt
        path("robots.txt", robots_txt),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + shop_urlpatterns
)