from django import template

register = template.Library()

@register.filter
def sub(value, value2):
    return float(value)-float(value2)

@register.filter
def price_decimals(value):
    try:
        result = '{:0>2.0f}'.format(float(value)%1*100)
    except:
        result = "00"
    return result 


@register.filter
def price_int(value):
    try:
        result = int(float(value)//1)
    except:
        result = ""
    return result
