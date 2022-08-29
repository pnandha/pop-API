from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField

class User(AbstractUser): 
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    mobileNumber = PhoneField(blank=True, help_text='Contact phone number')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
