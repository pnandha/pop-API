from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import User
from .models import Products

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobileNumber', 'userLocation', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class AllUserSerializer(serializers.ModelSerializer):
    saves = ProductSerializer(many=True, read_only=True)
    user_products = serializers.SerializerMethodField()
    
    def get_user_products(self, obj):
        user_products = Products.objects.filter(user_id=obj)
        serializer = ProductSerializer(user_products, many=True)
        return serializer.data
    
    def __init__(self, *args, **kwargs):
        products = kwargs.pop('products', None)
        super(AllUserSerializer, self).__init__(*args, **kwargs)
        if products is not None:
            self.fields['saves'] = ProductSerializer(products, many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobileNumber', 'userLocation', 'saves', 'user_products']

class SaveSerializer(serializers.ModelSerializer):
    saves = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'saves']