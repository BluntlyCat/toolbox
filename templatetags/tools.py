from django import template
from django.conf import settings
from toolbox.tools import is_local

register = template.Library()


@register.tag(name="IsLocal")
def is_local():
    return is_local(settings.FQDN)
