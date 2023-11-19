from django.contrib import admin
from .models import Product, ProductImage, Category, Review, Config
from .forms import ProductForm, ProductImageForm, CategoryForm, ReviewForm, ConfigForm
from import_export.admin import ExportActionModelAdmin
from django.urls import reverse


@admin.register(Product)
class ProductAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = (
        "title",
        "image_tag",
        "categories_tag",
        "reviews_tag",
        "description_tag",
        "asin",
        "price",
        "real_price",
        "visible",
        "featured",
        "slug",
        "url_tag",
        "url_affiliate_tag",
    )
    search_fields = ("title", "description", "asin", "slug")
    list_filter = ("visible", "featured", "categories")
    form = ProductForm
    list_per_page = 10

    def save_related(self, request, form, formsets, change):
        super(ProductAdmin, self).save_related(request, form, formsets, change)
        # Override save for add all parent categories of the choosen categories for the product in admin panel (dont work with model.save())
        for category in form.instance.categories.all():
            parents = category.all_parents()
            for parent in parents:
                form.instance.categories.add(parent.pk)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "position", "product")
    search_fields = ("product", "image")
    form = ProductImageForm
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "image_tag", "description_tag", "slug", "parent", "featured")
    search_fields = ("title", "slug")
    list_filter = ("parent",)
    form = CategoryForm
    list_per_page = 20


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "author_img_tag", "author", "text", "rating", "product")
    search_fields = ("title", "author", "text")
    list_filter = ("rating", "product")
    form = ReviewForm
    list_per_page = 10


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "canonical_url", "logo", "title_home", "title_decorator")
    search_fields = ("title_home", "name", "canonical_url")
    form = ConfigForm
    list_per_page = 10
