from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.contrib.sitemaps import ping_google

from tinymce.models import HTMLField


class WebComponentModel(models.Model):
    title = models.CharField(unique=True, blank=True, null=False, max_length=254)
    slug = models.CharField(unique=True, blank=True, null=False, max_length=254)
    description = models.TextField(blank=True, null=True, max_length=5000)
    meta_description = models.TextField(blank=True, null=True, max_length=5000)
    keywords = models.TextField(max_length=5000, null=True, blank=True)
    text = HTMLField(blank=True, null=True, max_length=20000)
    visible = models.BooleanField(blank=False, null=False, default=True)
    featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    publish_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    ext_ref = models.CharField(unique=True, blank=True, null=True, max_length=200)

    def save(self, *args, **kwargs):
        if self.id:
            # Add slug based in title
            self.slug = slugify(self.slug) if self.slug else slugify(self.title)

        super().save(*args, **kwargs)

        if self.visible:
            try:
                # Sitemap.xml - Ping Google on Updates
                ping_google()
            except Exception:
                pass

    # Django Admin Tags

    def description_tag(self):
        return self.description[:200] if self.description else None

    description_tag.short_description = "Description"

    def __str__(self):
        return f"{self.title}"

    class Meta:
        abstract = True


class WebsiteConfigModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(unique=True, blank=False, null=False, max_length=100)
    canonical_url = models.URLField(max_length=254, null=True, blank=True)

    logo = models.ImageField(null=True, blank=True)
    favicon = models.ImageField(null=True, blank=True)
    title_decorator = models.CharField(unique=True, blank=True, null=True, max_length=100)

    title_home = models.CharField(unique=True, blank=True, null=True, max_length=100)
    description_home = models.TextField(blank=True, null=True, max_length=5000)
    text_home = HTMLField(blank=True, null=True, max_length=20000)
    keywords_home = models.TextField(max_length=5000, blank=True, null=True)
    image_home = models.ImageField(null=True, blank=True)


class CategoryModel(WebComponentModel):
    class Meta:
        abstract = True
        verbose_name_plural = "categories"

    parent = models.ForeignKey("self", related_name="childs", on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, width_field="image_width", height_field="image_height")
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)

    def all_parents(self):
        # Return all parents until the root for the category
        parent_categories = []
        category = self
        while category.parent:
            parent_categories.append(category.parent)
            category = category.parent
        return parent_categories

        # def _get_parents(category):
        #     if category.parent:
        #         _get_parents(category.parent)
        #     parent_categories.append(category)

        # _get_parents(self)

    # Sitemap.xml

    def get_absolute_url(self):
        return reverse("category-slug", args=[self.slug])

    # Django Admin Tags

    def image_tag(self):
        return mark_safe(f'<img src="/media/{self.image}" width="100" height="100" />') if self.image else "No image"

    def description_tag(self):
        html = f"""
            <textarea style="width: 551px; height: 57px; position: relative;">{self.description}</textarea>
        """
        return mark_safe(html) if self.description else ""

    image_tag.short_description = "Image"
    description_tag.short_description = "Description"


class ImageModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(unique=False, blank=True, null=True, max_length=100, default="New Image")
    image = models.ImageField(null=True, blank=True, width_field="image_width", height_field="image_height")
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)

    # Django Admin Tags

    def image_tag(self):
        return mark_safe(f'<img src="/media/{self.image}" width="100" height="100" />') if self.image else "No image"
