from django.contrib.sitemaps import Sitemap
from .models import Product, Category

import datetime


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Category.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())

    def lastmod(self, obj):
        return obj.last_modified


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Product.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())

    def lastmod(self, obj):
        return obj.last_modified
