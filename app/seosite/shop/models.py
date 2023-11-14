from django.db import models
from tinymce.models import HTMLField
from django.utils.html import mark_safe
from django.utils.text import slugify


class WebComponentModel(models.Model):
    title = models.CharField(unique=True, blank=True, null=False, max_length=254)
    slug = models.CharField(unique=True, blank=True, null=False, max_length=254)
    description = models.TextField(blank=True, null=True, max_length=5000)
    meta_description = models.TextField(blank=True, null=True, max_length=5000)
    keywords = models.CharField(max_length=254, null=True, blank=True)
    text = HTMLField(blank=True, null=True, max_length=20000)
    faq = models.JSONField(blank=True, null=True, max_length=20000)
    featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    ext_ref = models.CharField(unique=True, blank=True, null=True, max_length=200)

    def description_tag(self):
        return self.description[:200] if self.description else None

    description_tag.short_description = "Description"

    def __str__(self):
        return f"{self.title}"

    class Meta:
        abstract = True


class Category(WebComponentModel):
    parent = models.ForeignKey("self", related_name="childs", on_delete=models.CASCADE, blank=True, null=True)
    # image = models.URLField(max_length=254, null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, width_field="image_width", height_field="image_height")

    def image_tag(self):
        return mark_safe(f'<img src="{self.image}" width="100" height="100" />') if self.image else None

    image_tag.short_description = "Image"

    def description_tag(self):
        html = f"""
            <textarea style="width: 551px; height: 57px; position: relative;">{self.description}</textarea>
        """
        return mark_safe(html) if self.description else None

    description_tag.short_description = "Description"

    def all_parents(self):
        # Return all parents until the root for the category
        parent_categories = []

        def _get_parents(category):
            if category.parent:
                _get_parents(category.parent)
            parent_categories.append(category)

        _get_parents(self)
        return parent_categories

    class Meta:
        verbose_name_plural = "categories"


class Product(WebComponentModel):
    visible = models.BooleanField(blank=False, null=False, default=True)
    categories = models.ManyToManyField(Category, related_name="products", symmetrical=False, blank=True)
    asin = models.CharField(max_length=20, unique=True, null=True)
    url = models.URLField(max_length=254, null=True, blank=True)
    url_affiliate = models.URLField(max_length=254, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    real_price = models.FloatField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)

    def image_tag(self):
        return (
            mark_safe(
                f'<a href=/admin/shop/productimage/{self.images.first().pk}><img src="{self.images.first().large}" width="80" height="80" /></a>'
            )
            if self.images.first()
            else None
        )

    image_tag.short_description = "Image"

    def url_tag(self):
        return mark_safe(f'<a href="{self.url}">{self.url[12:]}</a>') if self.url else None

    url_tag.short_description = "URL"

    def url_affiliate_tag(self):
        return (
            mark_safe(f'<a href="{self.url_affiliate}">{self.url_affiliate[12:]}</a>') if self.url_affiliate else None
        )

    url_affiliate_tag.short_description = "URL Affiliate"

    def description_tag(self):
        html = f"""
            <textarea style="width: 551px; height: 57px; position: relative;">{self.description}</textarea>
        """
        return mark_safe(html) if self.description else None

    description_tag.short_description = "Description"

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

    categories_tag.short_description = "Categories"

    def reviews_tag(self):
        return (
            mark_safe(
                "".join(
                    [f"<a href=/admin/shop/category/{review.pk}>{review.pk}</a> | " for review in self.reviews.all()]
                )
            )
            if self.reviews
            else None
        )

    reviews_tag.short_description = "Reviews"

    def save(self, *args, **kwargs):
        # Override save for add all parent categories of the choosen categories for the product
        # Doesn't works when is executed throught the admin. Correction is in the method save_related() on ProductAdmin() admin.py
        if self.id:
            for category in self.categories.all():
                parents = category.all_parents()
                for parent in parents:
                    self.categories.add(parent)
            # Add slug based in title
            self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)

    def create(self, data):
        product, created = Product.objects.update_or_create(asin=data.get("asin", None), defaults={data})
        return product

    def __str__(self):
        return f"{self.title[:50]}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.URLField(max_length=254, null=True, blank=True)
    thumb = models.URLField(max_length=254, null=True, blank=True)
    large = models.URLField(max_length=254, null=True, blank=True)
    medium = models.URLField(max_length=254, null=True, blank=True)
    small = models.URLField(max_length=254, null=True, blank=True)
    position = models.PositiveSmallIntegerField(null=False, default=0)

    def large_tag(self):
        return mark_safe(f'<img src="{self.large}" width="80" height="80" />') if self.large else None

    large_tag.short_description = "Large Image"

    def thumb_tag(self):
        return mark_safe(f'<img src="{self.thumb}" width="80" height="80" />') if self.thumb else None

    thumb_tag.short_description = "Thumb"

    def __str__(self):
        return f"{self.image}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(blank=False, null=False, max_length=200)
    text = models.TextField()
    author = models.CharField(max_length=64)
    author_img = models.URLField(max_length=254, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def author_img_tag(self):
        return mark_safe(f'<img src="{self.author_img}" width="50" height="50" />') if self.author_img else None

    author_img_tag.short_description = "Author Image"


class Config(models.Model):
    name = models.CharField(unique=True, blank=False, null=False, max_length=100)
    value = models.CharField(unique=True, blank=False, null=False, max_length=254)
