from django.urls import reverse
from django.conf import settings
from django.utils.html import mark_safe
from django.db import models

from common.models import WebsiteConfigModel, WebComponentModel, ImageModel


class Config(WebsiteConfigModel):
    pass


class Image(ImageModel):
    pass


class Page(WebComponentModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pages", blank=True, null=True
    )
    images = models.ManyToManyField(Image, related_name="pages", blank=True)

    # Sitemap.xml

    def get_absolute_url(self):
        return reverse("post-slug", args=[self.slug])

    # Tags

    def image_tag(self):
        return (
            mark_safe(f'<img src="/media/{self.images.first().image.url}" width="100" height="100" />')
            if self.images.first()
            else "No image"
        )

    image_tag.short_description = "Image"
