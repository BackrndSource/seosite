import datetime
from django import template

register = template.Library()


@register.filter
def posts(category, num=8):
    return (
        category.posts.filter(visible=True)
        .exclude(publish_date__gte=datetime.datetime.now())
        .order_by("-last_modified")
    )
