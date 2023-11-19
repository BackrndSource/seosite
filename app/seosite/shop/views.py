from .models import Category, Product, ProductImage, Review, Config

from django.views.generic import ListView, DetailView

from django.utils import timezone

import os


class HomeView(ListView):
    model = Category
    queryset = Category.objects.filter(visible=True)
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(visible=True).exclude(publish_date__gte=timezone.now())
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/product/list.html"


class ProductDetailView(DetailView):
    context_object_name = "product"
    queryset = Product.objects.filter(visible=True).exclude(publish_date__gte=timezone.now())
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/product/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.filter(visible=True)
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/category/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryDetailView(DetailView):
    context_object_name = "category"
    queryset = Category.objects.all()
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/category/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ALL PRODUCTS
        products = self.get_object().products.filter(visible=True).exclude(publish_date__gte=timezone.now())
        # REVIEWS
        reviews = []
        for product in products:
            reviews.append(product.reviews.first())
            if len(reviews) >= 10:
                break

        context["reviews"] = reviews

        context["featured_products"] = products.filter(featured=True).order_by(
            "-last_modified", "-rating_count", "-rating"
        )
        context["promo_products"] = products.filter(real_price__isnull=False).order_by(
            "-last_modified", "-rating_count", "-rating"
        )
        context["bestselling_products"] = products.filter(rating__gte=4).order_by(
            "-rating_count", "-last_modified", "-rating"
        )
        context["bestrated_products"] = products.filter(rating__gte=4).order_by(
            "-rating", "-rating_count", "-last_modified"
        )

        return context
