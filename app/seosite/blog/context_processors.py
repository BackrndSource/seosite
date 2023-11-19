from .models import Category, Config
from django.utils import timezone


def blog_config(request):
    return {
        "blog_config": Config.objects.first(),
        "blog_categories": Category.objects.filter(visible=True, parent=None).exclude(publish_date__gte=timezone.now()),
    }
