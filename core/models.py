from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings


class User(AbstractUser):
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=13, null=True)
    history = models.ManyToManyField("Product", through="BuyHistory")


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.FilePathField(path=settings.LOCAL_FILE_DIR)


class BuyHistory(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    product = models.ForeignKey("product", on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
