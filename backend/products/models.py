from django.db import models
import uuid
from django.conf import settings

class Category(models.Model): 
    name = models.CharField(max_length=255)

class Products(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trading_for = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 



