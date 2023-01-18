from django.contrib.gis.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phone_field import PhoneField
from products.models import Products


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}
        if not email:
            raise ValueError("Users must have an email address")
        user = User(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True, "userLocation": 'POINT (0 0)'}
        user = self.create_user(email=email, password=password, **extra_fields)
        return user

class User(AbstractUser): 
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    mobileNumber = PhoneField(blank=True, help_text='Contact phone number')
    saves = models.ManyToManyField(Products)
    userLocation = models.PointField()
    userStringLocation = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


