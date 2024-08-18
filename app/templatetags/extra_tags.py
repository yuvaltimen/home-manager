from django import template
from itertools import zip_longest

register = template.Library()


@register.filter(name='zip')
def zip_lists(a, b):
    return zip_longest(a, b)


@register.filter(name='replace_with_space')
def replace_with(value, to_replace):
    return value.replace(to_replace, " ")

