from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductImageViewSet, CategoryListView, CategoryDetailView, ProductDetailView
from .sitemaps import ProductSitemap, CategorySitemap
from django.urls import path
from django.contrib.sitemaps.views import sitemap

router = DefaultRouter()

router.register(r"shop/categories", CategoryViewSet)
router.register(r"shop/products", ProductViewSet)
router.register(r"shop/product-images", ProductImageViewSet)
        
sitemaps = {
    "categorias": CategorySitemap,
    "productos": ProductSitemap,
    # "reviews": ReviewSitemap
}

urlpatterns = [
    # path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='unique_slug'),
    path("categorias/", CategoryListView.as_view(), name="category-list"),
    path("categoria/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("producto/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    # Sitemap.xml
    path("sitemap-tienda-<section>.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap")
]
