from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    HomeView,
    PageListView,
    PageDetailView,
)
from .viewsets import PageViewSet, ConfigViewSet, ImageViewSet
from .sitemaps import PageSitemap


from django.contrib.sitemaps.views import index, sitemap

from .views import robots_txt

import os

from shop.urls import urlpatterns as shop_urlpatterns
from shop.urls import sitemaps as shop_sitemaps

from blog.urls import urlpatterns as blog_urlpatterns
from blog.urls import sitemaps as blog_sitemaps


SHOP_ACTIVE = os.getenv("SHOP_ACTIVE") == "True"
SHOP_HOME_URL = os.getenv("SHOP_HOME_URL") if os.getenv("SHOP_HOME_URL") else ""
BLOG_ACTIVE = os.getenv("BLOG_ACTIVE") == "True"
BLOG_HOME_URL = os.getenv("BLOG_HOME_URL") if os.getenv("BLOG_HOME_URL") else ""

SITE_PAGE_DETAIL_URL = os.getenv("SITE_PAGE_DETAIL_URL") if os.getenv("SITE_PAGE_DETAIL_URL") else "site-page"

router = DefaultRouter()
router.register(r"pages", PageViewSet)
router.register(r"config", ConfigViewSet)
router.register(r"images", ImageViewSet)

# Sitemap.xml
sitemaps = {
    "site-paginas": PageSitemap,
}
if SHOP_ACTIVE:
    [sitemaps.setdefault(key, value) for key, value in shop_sitemaps.items()]
if BLOG_ACTIVE:
    [sitemaps.setdefault(key, value) for key, value in blog_sitemaps.items()]


def getUrlPatterns():
    urlpatterns = [
        # REST API
        path("api/site/", include((router.urls, "site"))),
        # Page
        # path("paginas/", CategoryListView.as_view(), name="site-page-list"),
        path(
            f"<slug:slug>-{SITE_PAGE_DETAIL_URL}/",
            PageDetailView.as_view(),
            name="site-page-slug",
        ),
        # Sitemap.xml
        path(
            "sitemap.xml",
            index,
            {"sitemaps": sitemaps, "template_name": "sitemap_index.xml"},
            name="django.contrib.sitemaps.views.sitemap",
        ),
        path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
        # Robots.txt
        path("robots.txt", robots_txt),
    ]

    if BLOG_ACTIVE:
        urlpatterns = urlpatterns + blog_urlpatterns
    if SHOP_ACTIVE:
        urlpatterns = urlpatterns + shop_urlpatterns

    if SHOP_HOME_URL != "" and BLOG_HOME_URL != "":
        urlpatterns = urlpatterns + [path("", HomeView.as_view(), name="site-home")]

    return urlpatterns
