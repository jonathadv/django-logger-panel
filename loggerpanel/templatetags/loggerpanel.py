from logging import getLevelName

from django import template

register = template.Library()


@register.filter(name="log_level_name")
def log_level_name(value):
    """Removes all values of arg from the given string"""
    return getLevelName(value)
