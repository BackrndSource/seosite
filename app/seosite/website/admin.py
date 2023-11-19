from django.contrib import admin
from .models import Page, Image, Config
from import_export.admin import ExportActionModelAdmin


@admin.register(Page)
class PageAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = (
        "title",
        "image_tag",
        "description_tag",
        "visible",
        "featured",
        "slug",
    )
    search_fields = ("title", "description", "slug")
    list_filter = ("visible", "featured")
    list_per_page = 20


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "pages")
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
