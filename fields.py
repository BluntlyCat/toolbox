from django.db import models
from django.utils.translation import gettext as _
from django import forms
from .thumbnails import create_thumbnail, make_watermark, get_image_django_type, read_image_bytes


class ResponsiveImage(object):
    pass


class ResponsiveImageFormField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ResponsiveImageField(models.ImageField):
    description = _('Responsive image')

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 4096
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']

        return name, path, args, kwargs

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'varchar'
        else:
            return 'varchar'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return None

    def to_python(self, value):
        if isinstance(value, ResponsiveImage):
            return value

        if value is None:
            return value

        return None

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': ResponsiveImageFormField,
            **kwargs,
        })

    def save_form_data(self, instance, data):
        super().save_form_data(instance, data)
