from django.template import Library

register = Library()

@register.filter
def get_len( value ):
  return len( value )
