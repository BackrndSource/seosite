from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.authtoken.views import obtain_auth_token

from django.contrib.sitemaps.views import index, sitemap

from common.views import robots_txt, HomeView

from shop.urls import urlpatterns as shop_urlpatterns
from shop.urls import sitemaps as shop_sitemaps

from blog.urls import urlpatterns as blog_urlpatterns
from blog.urls import sitemaps as blog_sitemaps

import os


SHOP_ACTIVE = os.getenv("SHOP_ACTIVE") == "True"
SHOP_HOME_URL = os.getenv("SHOP_HOME_URL") if os.getenv("SHOP_HOME_URL") else ""
BLOG_ACTIVE = os.getenv("BLOG_ACTIVE") == "True"
BLOG_HOME_URL = os.getenv("BLOG_HOME_URL") if os.getenv("BLOG_HOME_URL") else ""

sitemaps = {}
if SHOP_ACTIVE:
    [sitemaps.setdefault(key, value) for key, value in shop_sitemaps.items()]
if BLOG_ACTIVE:
    [sitemaps.setdefault(key, value) for key, value in blog_sitemaps.items()]

urlpatterns = (
    [
        # Admin
        path("admin/", admin.site.urls),
        # REST API
        path("api/auth/", obtain_auth_token),
        # Sitemap.xml
        path("sitemap.xml", index, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
        path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
        # Robots.txt
        path("robots.txt", robots_txt),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
if BLOG_ACTIVE:
    urlpatterns = urlpatterns + blog_urlpatterns
if SHOP_ACTIVE:
    urlpatterns = urlpatterns + shop_urlpatterns

if SHOP_HOME_URL != "" and BLOG_HOME_URL != "":
    urlpatterns = urlpatterns + [path("", HomeView.as_view(), name="site-home")]
