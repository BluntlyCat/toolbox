# coding: utf-8
import logging
import os

from django.core.files.base import File
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile, SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import ugettext as _
from django.conf import settings

from PIL import Image
from io import BytesIO

logger = logging.getLogger('manager')

__author__ = 'mhaze'


class ImageType(object):
    image = 'image'
    unknown = 'unknown'

    django = {
        'image/jpeg': {'pil': 'jpeg', 'fe': 'jpg'},
        'image/png': {'pil': 'png', 'fe': 'png'},
        'image/gif': {'pil': 'gif', 'fe': 'gif'},
        'image/bmp': {'pil': 'bmp', 'fe': 'bmp'},
    }

    pil = {
        'JPEG': {'pil': 'jpeg', 'fe': 'jpg'},
        'PNG': {'pil': 'png', 'fe': 'png'},
        'GIF': {'pil': 'gif', 'fe': 'gif'},
        'BMP': {'pil': 'bmp', 'fe': 'bmp'},
    }


def file_type(type_of_file):
    # Check if ftype is a known image
    if type_of_file in ImageType.django:
        return ImageType.image

    elif type_of_file in ImageType.pil:
        return ImageType.image

    else:
        return ImageType.unknown


def get_image_extension(type_of_file):
    if type_of_file in ImageType.django:
        return ImageType.django[type_of_file]

    elif type_of_file in ImageType.pil:
        return ImageType.pil[type_of_file]

    else:
        return None


def get_image_django_type(file_field, byte_io):
    if isinstance(file_field.file, InMemoryUploadedFile):
        return file_field.file.content_type

    elif isinstance(file_field.file, TemporaryUploadedFile):
        return file_field.file.content_type

    elif isinstance(file_field.file, File):
        return Image.open(byte_io).format

    else:
        raise ValueError(_('Unknown type of file instance'))


def read_image_bytes(file_field: ImageFieldFile):
    byte_io = BytesIO(file_field.read())
    return byte_io


def create_thumbnail(image_bytes: BytesIO, django_type: str, file_field_name: str, width: int = 0, height: int = 0):
    """
    :param image_bytes:
    :param django_type
    :param file_field_name
    :param width:
    :param height:
    :return:
    """
    # original code for this method came from
    # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

    # Open original photo which we want to thumbnail using PIL's Image
    image = Image.open(image_bytes)

    # Set our max thumbnail size in a tuple (max width, max height)
    if not width and not height:
        thumbnail_size = (
            image.width,
            image.height,
        )

    elif not width and height:
        thumbnail_size = (
            image.width * (height / image.height),
            height,
        )

    elif width and not height:
        thumbnail_size = (
            width,
            image.height * (width / image.width),
        )

    else:
        thumbnail_size = (
            width,
            height,
        )

    width = thumbnail_size[0]
    height = thumbnail_size[1]

    logger.debug('Set image size %d/%d' % (width, height))

    if file_type(django_type) == ImageType.image:
        pil_type = get_image_extension(django_type)['pil']

    else:
        raise Exception(file_type(django_type))

    # Convert to RGB if necessary
    # Thanks to Limodou on DjangoSnippets.org
    # http://www.djangosnippets.org/snippets/20/
    #
    # I commented this part since it messes up my png files
    #
    # if image.mode not in ('L', 'RGB'):
    #    image = image.convert('RGB')

    # We use our PIL Image object to create the thumbnail, which already
    # has a thumbnail() convenience method that constrains proportions.
    # Additionally, we use Image.ANTIALIAS to make the image look better.
    # Without antialiasing the image pattern artifacts may result.
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)

    # Save the thumbnail
    temp_handle = BytesIO()
    image.save(temp_handle, pil_type)
    temp_handle.seek(0)

    # Save image to a SimpleUploadedFile which can be saved into ImageField
    suf = SimpleUploadedFile(os.path.split(file_field_name)[-1], temp_handle.read(), content_type=django_type)

    return suf


def make_watermark(file_field, percentage_size=0.3, opacity=3, offset_x=10, offset_y=10):
    image = Image.open(file_field.file)
    watermark = Image.open(settings.WATERMARK_IMAGE)

    rgba_image = image.convert('RGB')
    rgba_watermark = watermark.convert('RGBA')

    image_x, image_y = rgba_image.size
    watermark_x, watermark_y = rgba_watermark.size

    new_size_x = int(image_x * percentage_size)
    new_size_y = int((new_size_x / watermark_x) * watermark_y)
    rgba_watermark = rgba_watermark.resize((new_size_x, new_size_y), resample=Image.ANTIALIAS)

    rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: max(x, opacity))
    rgba_watermark.putalpha(rgba_watermark_mask)

    wm_position_x = image_x - new_size_x - offset_x
    wm_position_y = image_y - new_size_y - offset_y
    rgba_image.paste(rgba_watermark, (wm_position_x, wm_position_y), rgba_watermark_mask)

    if isinstance(file_field.file, InMemoryUploadedFile):
        django_type = file_field.file.content_type

    elif isinstance(file_field.file, File):
        django_type = image.format

    else:
        raise ValueError(_('Unknown type of file instance'))

    if file_type(django_type) == ImageType.image:
        pil_type = get_image_extension(django_type)['pil']

    else:
        raise Exception(file_type(django_type), file_field.name)

    temp_handle = BytesIO()
    rgba_image.save(temp_handle, pil_type)
    temp_handle.seek(0)

    # Save image to a SimpleUploadedFile which can be saved into ImageField
    suf = SimpleUploadedFile(os.path.split(file_field.name)[-1], temp_handle.read(), content_type=django_type)

    return suf
