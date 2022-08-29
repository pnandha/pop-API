from rest_framework import serializers
from .models import Products

class Producterializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'email', 'mobileNumber', 'password']
