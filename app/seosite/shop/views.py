from typing import Any
from django.db import models
from .models import Category, Product, ProductImage, Review, Config

from django.views.generic import ListView, DetailView

import datetime

import os


class HomeView(ListView):
    queryset = Category.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/home.html"


class ProductListView(ListView):
    queryset = (
        Product.objects.filter(visible=True)
        .exclude(publish_date__gte=datetime.datetime.now())
        .order_by("-last_modified", "-rating_count", "-rating")
    )
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/product/list.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/product/detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())


class CategoryListView(ListView):
    queryset = Category.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/category/list.html"


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = "category"
    template_name = f"shop/{os.getenv('SHOP_TEMPLATE')}/views/category/detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ALL PRODUCTS
        products = self.get_object().products.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())
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
