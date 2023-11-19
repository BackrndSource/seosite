from django.utils import timezone
from django import template

register = template.Library()


@register.filter
def childs(category):
    return category.childs.filter(visible=True).exclude(publish_date__gte=timezone.now()).order_by("featured")
