import os, datetime

from .models import Config, Page


def site_config(request):
    return {
        "SITE_GTAG_ID": os.getenv("SITE_GTAG_ID"),
        "SHOP_ACTIVE": os.getenv("SHOP_ACTIVE") == "True",
        "BLOG_ACTIVE": os.getenv("BLOG_ACTIVE") == "True",
        "site_config": Config.objects.first(),
        "site_pages": Page.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now()),
    }
