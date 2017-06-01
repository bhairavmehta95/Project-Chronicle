from django import template

register = template.Library()


@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)