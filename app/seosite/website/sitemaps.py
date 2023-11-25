from django.contrib.sitemaps import Sitemap
from .models import Page

import datetime


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Page.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())

    def lastmod(self, obj):
        return obj.last_modified
