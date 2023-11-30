from django.contrib.sitemaps import Sitemap
from .models import Post, Category

import datetime


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Category.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())

    def lastmod(self, obj):
        return obj.last_modified


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Post.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())

    def lastmod(self, obj):
        return obj.last_modified
