import os
from django.db import models
from django.db.models.fields.files import FieldFile
from .thumbnails import create_thumbnail, make_watermark, get_image_django_type, read_image_bytes
from .fields import ResponsiveImageField

# Create your models here.


class ResponsiveImage(models.Model):
    original_image = models.ImageField(upload_to='responsive_images/original_images/')
    old_image_path = models.CharField(max_length=1024)
    watermark = models.BooleanField(default=True)
    has_watermark = models.BooleanField(default=False)
    alt = models.CharField(max_length=128)

    xl = models.ImageField(upload_to='responsive_images/xl/')
    lg = models.ImageField(upload_to='responsive_images/lg/')
    md = models.ImageField(upload_to='responsive_images/md/')
    sm = models.ImageField(upload_to='responsive_images/sm/')
    xs = models.ImageField(upload_to='responsive_images/xs/')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__byte_io = None
        self.__django_type = None
        self.__image_name = None

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            self.__delete_files()

        if self.original_image_changed or self.watermark_changed:
            self.xl = create_thumbnail(self.byte_io, self.django_type, self.image_name, 1200)
            self.lg = create_thumbnail(self.byte_io, self.django_type, self.image_name, 992)
            self.md = create_thumbnail(self.byte_io, self.django_type, self.image_name, 768)
            self.sm = create_thumbnail(self.byte_io, self.django_type, self.image_name, 576)
            self.xs = create_thumbnail(self.byte_io, self.django_type, self.image_name, 320)

            self.old_image_path = self._generate_path(self.original_image, 'responsive_images', 'original_images')

        if self.original_image_changed and self.watermark or self.add_watermark:
            self.xl = make_watermark(self.xl)
            self.lg = make_watermark(self.lg)
            self.md = make_watermark(self.md)
            self.sm = make_watermark(self.sm)
            self.xs = make_watermark(self.xs)

        self.has_watermark = self.watermark

        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.__delete_files(True)
        super().delete(using, keep_parents)

    def __delete_files(self, force_delete: bool = False):
        if self.original_image_changed or force_delete:
            self._delete_file(self.old_image_path)

        if self.original_image_changed or self.watermark_changed or force_delete:
            if self.xl:
                self._delete_file(self.xl.path)

            if self.lg:
                self._delete_file(self.lg.path)

            if self.md:
                self._delete_file(self.md.path)

            if self.sm:
                self._delete_file(self.sm.path)

            if self.xs:
                self._delete_file(self.xs.path)

    @staticmethod
    def _delete_file(file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)

    @staticmethod
    def _generate_path(image_field: FieldFile, *args):
        paths = os.path.split(image_field.path)
        return os.path.join(paths[:-1][0], os.path.sep.join(args), paths[len(paths) - 1].replace(' ', '_'))

    def __str__(self):
        return str(self.original_image)

    @property
    def name(self):
        return self.original_image.name

    @name.setter
    def name(self, value):
        self.original_image.name = value

    @property
    def path(self):
        return self.original_image.path

    @property
    def byte_io(self):
        if not self.__byte_io:
            self.__byte_io = read_image_bytes(self.original_image)

        return self.__byte_io

    @property
    def django_type(self):
        if not self.__django_type:
            self.__django_type = get_image_django_type(self.original_image, self.__byte_io)

        return self.__django_type

    @property
    def image_name(self):
        if not self.__image_name and self.original_image:
            self.__image_name = self.original_image.name

        return self.__image_name

    @property
    def original_image_changed(self):
        return self.original_image and self.original_image.path != self.old_image_path

    @property
    def add_watermark(self):
        return not self.has_watermark and self.watermark

    @property
    def remove_watermark(self):
        return self.has_watermark and not self.watermark

    @property
    def watermark_changed(self):
        return self.watermark != self.has_watermark

    class Meta:
        abstract = True


class ImageFieldTest(models.Model):
    image = ResponsiveImageField(upload_to='test_images')
