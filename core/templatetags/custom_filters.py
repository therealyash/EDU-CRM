from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Add a CSS class to a form field
    Usage: {{ form.field|add_class:"my-class" }}
    """
    if isinstance(value, BoundField):
        # If it's a form field, modify the widget attrs
        existing_class = value.field.widget.attrs.get('class', '')
        new_class = f"{existing_class} {arg}".strip()
        value.field.widget.attrs['class'] = new_class
        return value
    return value
