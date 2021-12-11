from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class User(AbstractUser):
    pass

class Bookmark(TimeStampedModel):
    title = models.CharField(max_length=9999)
    url = models.URLField(verbose_name='bookmark_url')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)

