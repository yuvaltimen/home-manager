from django import template
from itertools import zip_longest

register = template.Library()


@register.filter(name='zip')
def zip_lists(a, b):
    return zip_longest(a, b)
