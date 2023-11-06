from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from shop.views import *
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

# Create a router for the viewsets
router = DefaultRouter()
router.register(r"shop/categories", CategoryViewSet)
router.register(r"shop/products", ProductViewSet)
router.register(r"shop/product-images", ProductImageViewSet)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", include((router.urls, "api"))),  # Include the router URLs
        path("api/auth/", obtain_auth_token),
        # Frontend
        path("categories/", CategoryListView.as_view(), name="category-list"),
        path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
        path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
        # path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='unique_slug'),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

# Additional URL patterns for custom API views can be added here
