from django.test import TestCase
from .models import ImageFieldTest

# Create your tests here.


class ResponsiveImageTest(TestCase):
    __image = ImageFieldTest(image='D:\\mhaze\\Development\\PyCharm\\portfolio\\static\\images\\watermark.jpg')

    def test_save_image(self):
        self.__image.save()

        image = ImageFieldTest.objects.first()
        self.assertEqual(image.pk, 1)
