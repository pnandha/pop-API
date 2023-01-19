from django.contrib.gis.db import models
import uuid
from django.conf import settings
from django.utils import timezone


def upload_to(instance, filename):
    return 'images/productImages/{filename}'.format(filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=255)


class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trading_for = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.PointField()
    stringPostalCode = models.CharField(max_length=10)
    expire = models.DateField(auto_now_add=True, default=timezone.now())
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
