from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    HomeView,
    # CategoryListView,
    CategoryDetailView,
    ProductDetailView,
)
from .viewsets import (
    CategoryViewSet,
    ProductViewSet,
    ProductImageViewSet,
)
from .sitemaps import ProductSitemap, CategorySitemap

import os

SHOP_HOME_URL = os.getenv("SHOP_HOME_URL") if os.getenv("SHOP_HOME_URL") else ""
SHOP_CATEGORY_LIST_URL = os.getenv("SHOP_CATEGORY_LIST_URL") if os.getenv("SHOP_CATEGORY_LIST_URL") else "categories/"
SHOP_CATEGORY_DETAIL_URL = os.getenv("SHOP_CATEGORY_DETAIL_URL") if os.getenv("SHOP_CATEGORY_DETAIL_URL") else "c/"
SHOP_PRODUCT_LIST_URL = os.getenv("SHOP_PRODUCT_LIST_URL") if os.getenv("SHOP_PRODUCT_LIST_URL") else "products/"
SHOP_PRODUCT_DETAIL_URL = os.getenv("SHOP_PRODUCT_DETAIL_URL") if os.getenv("SHOP_PRODUCT_DETAIL_URL") else "p/"


BLOG_ACTIVE = os.getenv("BLOG_ACTIVE") == "True"

router = DefaultRouter()

router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"product-images", ProductImageViewSet)

# Sitemap.xml
sitemaps = {
    "tienda-categorias": CategorySitemap,
    "tienda-productos": ProductSitemap,
}

urlpatterns = [
    # REST API
    path("api/shop/", include((router.urls, "shop"))),
    # Category
    path(f"{SHOP_HOME_URL}", HomeView.as_view(), name="shop-home"),
    # path("categorias/", CategoryListView.as_view(), name="category-list"),
    path(f"{SHOP_HOME_URL}{SHOP_CATEGORY_DETAIL_URL}<slug:slug>/", CategoryDetailView.as_view(), name="category-slug"),
    # Product
    path(f"{SHOP_HOME_URL}{SHOP_PRODUCT_DETAIL_URL}<slug:slug>/", ProductDetailView.as_view(), name="product-slug"),
]
