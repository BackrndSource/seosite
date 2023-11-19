from django.utils import timezone
from django import template

register = template.Library()


@register.filter
def posts(category, num=8):
    return category.posts.filter(visible=True)
