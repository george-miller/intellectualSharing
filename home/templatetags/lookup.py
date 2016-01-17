from django.template import Library

register = Library()

@register.filter
def lookup(d, key):
    return d[key]