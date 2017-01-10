from django import template

from main import helpers

register = template.Library()

@register.filter
def pretty_html(value):
    return helpers.pretty_html(value)


@register.filter
def keyvalue(dict, key):  
    if key in dict:  
        return dict[key]
    return ''