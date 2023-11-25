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
    name = models.CharField(max_length=254, null=False, blank=False, default="New Page")

    # Sitemap.xml

    def get_absolute_url(self):
        return reverse("site-page-slug", args=[self.slug])
