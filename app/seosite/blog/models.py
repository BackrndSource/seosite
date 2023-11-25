from django.db import models
from common.models import WebsiteConfigModel, WebComponentModel, CategoryModel, ImageModel
from django.utils.html import mark_safe
from django.urls import reverse
from django.conf import settings


class Config(WebsiteConfigModel):
    pass


class Image(ImageModel):
    pass


class Category(CategoryModel):
    # Sitemap.xml
    def get_absolute_url(self):
        return reverse("blog-category-slug", args=[self.slug])


class Post(WebComponentModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts", blank=True, null=True
    )
    categories = models.ManyToManyField(Category, related_name="posts", blank=True)
    images = models.ManyToManyField(Image, related_name="posts", blank=True)

    def save(self, *args, **kwargs):
        # Override save for add all parent categories of the choosen categories for the product
        # Doesn't works when is executed throught the admin. Correction is in the method save_related() on ProductAdmin() admin.py
        if self.id:
            for category in self.categories.all():
                parents = category.all_parents()
                for parent in parents:
                    self.categories.add(parent)

        super().save(*args, **kwargs)

    # Sitemap.xml

    def get_absolute_url(self):
        return reverse("blog-post-slug", args=[self.slug])

    # Django Admin Tags

    def categories_tag(self):
        return (
            mark_safe(
                "".join(
                    [
                        f"<a href=/admin/blog/category/{category.pk}>{category.title}</a> | "
                        for category in self.categories.all()
                    ]
                )
            )
            if self.categories
            else None
        )

    def comments_tag(self):
        return (
            mark_safe(
                "".join(
                    [f"<a href=/admin/blog/comment/{comment.pk}>{comment.pk}</a> | " for comment in self.comments.all()]
                )
            )
            if self.comments
            else None
        )

    def image_tag(self):
        return (
            mark_safe(f'<img src="/media/{self.images.first().image.url}" width="100" height="100" />')
            if self.images.first()
            else "No image"
        )

    categories_tag.short_description = "Categories"
    comments_tag.short_description = "Comments"
    image_tag.short_description = "Image"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(blank=False, null=False, max_length=200)
    text = models.TextField()
    author = models.CharField(max_length=64)
    author_img = models.URLField(max_length=254, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, null=False)

    # Django Admin Tags

    def author_img_tag(self):
        return mark_safe(f'<img src="{self.author_img}" width="32" height="32" />') if self.author_img else None

    author_img_tag.short_description = "Author Image"

    def __str__(self):
        return f"{self.title[:50]}"
