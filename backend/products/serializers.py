from rest_framework import serializers
from .models import Products, Category

class ProductSerializer(serializers.ModelSerializer):
    is_saved = serializers.BooleanField()
    class Meta:
        model = Products
        extra_kwargs = {'is_saved': {'required': False, "allow_null": True}} 
        fields = ['id', 'name', 'trading_for', 'description', 'location', 'user_id', 'category', 'image_url', 'expire', 'is_saved']


class ProductCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        extra_kwargs = {'image_url': {'required': True}} 
        fields = ['id', 'name', 'trading_for', 'description', 'location', 'user_id', 'category', 'image_url', 'expire']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
