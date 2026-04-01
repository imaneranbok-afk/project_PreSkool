# faculty/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Récupère une valeur dans un dictionnaire"""
    if dictionary is None:
        return None
    return dictionary.get(key)