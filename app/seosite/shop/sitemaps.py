from django.contrib.sitemaps import Sitemap
from .models import Product, Category, ProductImage

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.filter(visible=True)

    def lastmod(self, obj):
        return obj.last_modified

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Product.objects.filter(visible=True)

    def lastmod(self, obj):
        return obj.last_modified

# class ReviewSitemap(Sitemap):
#     changefreq = "daily"
#     priority = 0.5

#     def items(self):
#         return Review.objects.filter()

#     def lastmod(self, obj):
#         return obj.last_modified