import os

from .models import Config


def site_config(request):
    return {
        "SITE_GTAG_ID": os.getenv("SITE_GTAG_ID"),
        "SHOP_ACTIVE": os.getenv("SHOP_ACTIVE") == "True",
        "BLOG_ACTIVE": os.getenv("BLOG_ACTIVE") == "True",
        "site_config": Config.objects.first(),
    }
