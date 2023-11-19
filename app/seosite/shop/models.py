from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse
from common.models import WebComponentModel, CategoryModel, WebsiteConfigModel


class Config(WebsiteConfigModel):
    pass


class Category(CategoryModel):
    pass


class Product(WebComponentModel):
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    asin = models.CharField(max_length=20, unique=True, null=True)
    url = models.URLField(max_length=254, null=True, blank=True)
    url_affiliate = models.URLField(max_length=254, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    real_price = models.FloatField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Override save for add all parent categories of the choosen categories for the product
        # Doesn't works when is executed throught the admin. Correction is in the method save_related() on ProductAdmin() admin.py
        if self.id:
            for category in self.categories.all():
                parents = category.all_parents()
                for parent in parents:
                    self.categories.add(parent)

        super().save(*args, **kwargs)

    def create(self, data):
        product, created = Product.objects.update_or_create(asin=data.get("asin", None), defaults={data})
        return product

    # Sitemap.xml

    def get_absolute_url(self):
        return reverse("product-slug", args=[self.slug])

    # Django Admin Tags

    def image_tag(self):
        return (
            mark_safe(
                f'<a href=/admin/shop/productimage/{self.images.first().pk}><img src="{self.images.first().small}" width="80" height="80" /></a>'
            )
            if self.images.first()
            else None
        )

    def url_tag(self):
        return mark_safe(f'<a href="{self.url}">{self.url[12:]}</a>') if self.url else None

    def url_affiliate_tag(self):
        return (
            mark_safe(f'<a href="{self.url_affiliate}">{self.url_affiliate[12:]}</a>') if self.url_affiliate else None
        )

    def categories_tag(self):
        return (
            mark_safe(
                "".join(
                    [
                        f"<a href=/admin/shop/category/{category.pk}>{category.title}</a> | "
                        for category in self.categories.all()
                    ]
                )
            )
            if self.categories
            else None
        )

    def reviews_tag(self):
        return (
            mark_safe(
                "".join([f"<a href=/admin/shop/review/{review.pk}>{review.pk}</a> | " for review in self.reviews.all()])
            )
            if self.reviews
            else None
        )

    image_tag.short_description = "Image"
    url_tag.short_description = "URL"
    url_affiliate_tag.short_description = "URL Affiliate"
    categories_tag.short_description = "Categories"
    reviews_tag.short_description = "Reviews"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.URLField(max_length=254, null=True, blank=True)
    thumb = models.URLField(max_length=254, null=True, blank=True)
    large = models.URLField(max_length=254, null=True, blank=True)
    medium = models.URLField(max_length=254, null=True, blank=True)
    small = models.URLField(max_length=254, null=True, blank=True)
    position = models.PositiveSmallIntegerField(null=False, default=0)

    # Sitemap.xml

    def get_absolute_url(self):
        return reverse("productimage-detail", args=[self.pk])

    # Django Admin Tags

    def image_tag(self):
        return mark_safe(f'<img src="{self.small}" width="80" height="80" />') if self.small else None

    image_tag.short_description = "Image"

    def __str__(self):
        return f"{self.product.title[:50]}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(blank=False, null=False, max_length=200)
    text = models.TextField()
    author = models.CharField(max_length=64)
    author_img = models.URLField(max_length=254, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, null=False)

    # Django Admin Tags

    def author_img_tag(self):
        return mark_safe(f'<img src="{self.author_img}" width="50" height="50" />') if self.author_img else None

    author_img_tag.short_description = "Author Image"

    def __str__(self):
        return f"{self.title[:50]}"
