from django import template

register = template.Library()

@register.filter
def get_extension(value):
    return value.split('.')[-1] if '.' in value else ''
