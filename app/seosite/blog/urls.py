from rest_framework.routers import DefaultRouter
from .views import (
    HomeView,
    # CategoryListView,
    CategoryDetailView,
    PostDetailView,
)
from .viewsets import (
    CategoryViewSet,
    PostViewSet,
    ImageViewSet,
)
from .sitemaps import PostSitemap, CategorySitemap
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

import os

BLOG_HOME_URL = os.getenv("BLOG_HOME_URL") if os.getenv("BLOG_HOME_URL") else ""
BLOG_CATEGORY_LIST_URL = os.getenv("BLOG_CATEGORY_LIST_URL") if os.getenv("BLOG_CATEGORY_LIST_URL") else "categories/"
BLOG_CATEGORY_DETAIL_URL = os.getenv("BLOG_CATEGORY_DETAIL_URL") if os.getenv("BLOG_CATEGORY_DETAIL_URL") else "c/"
BLOG_POST_LIST_URL = os.getenv("BLOG_POST_LIST_URL") if os.getenv("BLOG_POST_LIST_URL") else "posts/"
BLOG_POST_DETAIL_URL = os.getenv("BLOG_POST_DETAIL_URL") if os.getenv("BLOG_POST_DETAIL_URL") else "p/"

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="blog-category")
router.register(r"posts", PostViewSet)
router.register(r"images", ImageViewSet)

# Sitemap.xml
sitemaps = {
    "blog-categorias": CategorySitemap,
    "blog-posts": PostSitemap,
}

urlpatterns = [
    # REST API
    path("api/blog/", include((router.urls, "blog"))),
    # Category
    path(f"{BLOG_HOME_URL}", HomeView.as_view(), name="blog-home"),
    # path("blog/categorias/", CategoryListView.as_view(), name="category-list"),
    path(
        f"{BLOG_HOME_URL}{BLOG_CATEGORY_DETAIL_URL}<slug:slug>/",
        CategoryDetailView.as_view(),
        name="blog-category-slug",
    ),
    # Post
    path(f"{BLOG_HOME_URL}{BLOG_POST_DETAIL_URL}<slug:slug>/", PostDetailView.as_view(), name="blog-post-slug"),
]
