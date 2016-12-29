from django import template

register = template.Library()

@register.filter(name='getId')
def getId(value):
    return str(value['_id'])