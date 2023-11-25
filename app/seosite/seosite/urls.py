from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.authtoken.views import obtain_auth_token

from website.urls import getUrlPatterns

urlpatterns = (
    [
        # Admin
        path("admin/", admin.site.urls),
        # REST API
        path("api/auth/", obtain_auth_token),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + getUrlPatterns()
)
