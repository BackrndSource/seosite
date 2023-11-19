from django.contrib.sitemaps import Sitemap
from .models import Post, Category


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.filter(visible=True)

    def lastmod(self, obj):
        return obj.last_modified


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Post.objects.filter(visible=True)

    def lastmod(self, obj):
        return obj.last_modified
