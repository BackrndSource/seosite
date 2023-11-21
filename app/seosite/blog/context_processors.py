from .models import Category, Config
import datetime


def blog_config(request):
    return {
        "blog_config": Config.objects.first(),
        "blog_categories": Category.objects.filter(visible=True, parent=None).exclude(
            publish_date__gte=datetime.datetime.now()
        ),
    }
