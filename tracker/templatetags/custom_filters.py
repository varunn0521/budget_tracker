from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, BoundField):  # Only process form fields
        return field.as_widget(attrs={"class": css_class})
    return field  # Return as-is if not a form field
