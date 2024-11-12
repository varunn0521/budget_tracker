# custom_filters.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Add a CSS class to a form field widget.
    """
    if hasattr(field, 'widget'):
        field.widget.attrs.update({'class': css_class})
    return field
