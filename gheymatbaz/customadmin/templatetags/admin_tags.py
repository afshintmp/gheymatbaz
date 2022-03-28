from django import template

register = template.Library()


@register.simple_tag(name='get_admin_sidebar')
def get_admin_sidebar():
    return "hello word!"
