import datetime
from django import template

register = template.Library()


@register.filter
def childs(category):
    return category.childs.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now()).order_by("featured")
