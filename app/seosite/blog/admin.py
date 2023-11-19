from django.contrib import admin
from .models import Category, Post, Image, Comment, Config
from import_export.admin import ExportActionModelAdmin
from django.urls import reverse


@admin.register(Post)
class PostAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = (
        "title",
        "image_tag",
        "categories_tag",
        "comments_tag",
        "description_tag",
        "visible",
        "featured",
        "slug",
    )
    search_fields = ("title", "description", "slug")
    list_filter = ("visible", "featured", "categories")
    list_per_page = 20

    def save_related(self, request, form, formsets, change):
        super(PostAdmin, self).save_related(request, form, formsets, change)
        # Override save for add all parent categories of the choosen categories for the product in admin panel (dont work with model.save())
        for category in form.instance.categories.all():
            parents = category.all_parents()
            for parent in parents:
                form.instance.categories.add(parent.pk)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "posts")
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "image_tag", "description_tag", "slug", "parent", "featured")
    search_fields = ("title", "slug")
    list_filter = ("parent",)
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("title", "author_img_tag", "author", "text", "post")
    search_fields = ("title", "author", "text")
    list_filter = ("author", "post")
    list_per_page = 20


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "canonical_url",
        "logo",
        "title_home",
        "title_decorator",
    )
    search_fields = ("title_home", "name", "canonical_url")
    list_per_page = 20
