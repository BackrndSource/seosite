from .models import Category, Config
from django.utils import timezone


def shop_config(request):
    return {
        "shop_config": Config.objects.first(),
        "shop_categories": Category.objects.filter(visible=True, parent=None).exclude(publish_date__gte=timezone.now()),
    }
