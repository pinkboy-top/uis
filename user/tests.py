import uuid

from django.test import TestCase
from user.models import Img, ImgType, Option, OptionType


# Create your tests here.


def test_create_img():
    img = Img()
    img.img_url = "dsadsadsa"
    img.img_type = Option.objects.filter(id=1)
    img.save()
    return img


if __name__ == "__mian__":
    print(test_create_img())
