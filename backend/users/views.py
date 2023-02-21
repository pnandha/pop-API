import json
from multiprocessing import AuthenticationError
from urllib import response
from uuid import UUID
import uuid
from xml.dom import ValidationErr
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.core.serializers.json import DjangoJSONEncoder
from products.serializers import ProductSerializer
from .models import Products
import jwt, datetime
from django.http import Http404
from jwt import PyJWT

from .models import User

from .serializers import AllUserSerializer, SaveSerializer, UserSerializer

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
     serializer = UserSerializer(data=request.data)
     serializer.is_valid(raise_exception=True)
     email = request.data.get('email')
     if User.objects.filter(email=email).exists():
            raise ValidationErr({'email': 'Email already exists'})
     serializer.save()
     return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')   
        payload = {
            'id' :  str(user.id),
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }


        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        
        user = User.objects.filter(id=uuid.UUID(payload['id'])).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successs'
        }
        return response

class UserInfoView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        id = request.GET.get('id')
        user = User.objects.filter(id=uuid.UUID(id)).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class SaveProdView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        
        user = User.objects.get(id=request.data['user_id'])
        product = Products.objects.get(id=request.data['saves'])
        user.saves.add(product)
        user.save()
        return Response({'message': 'Product added to saves'})
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=uuid.UUID(payload['id'])).first()
        saved_products = user.saves.all()
        for product in saved_products:
                product.is_saved = True
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 10))
        start = (page - 1) * page_size
        end = page * page_size
        total_products = saved_products.count()
        serializer = ProductSerializer(saved_products[start : end] ,many=True)
        return Response(
            {
            "page":  page,
            "page_size": page_size,
            "content": serializer.data,
            "product_total": total_products,
            }
        )


class UpdateUserView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=uuid.UUID(payload['id'])).first()
        print(request.data)
        user.userLocation = request.data['location']
        user.userStringLocation = request.data['stringLocation']
        user.name = request.data['name']
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
        

class UnsaveProductView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=uuid.UUID(payload['id'])).first()
        product_id = request.data.get('product_id')
        product = Products.objects.filter(id=product_id).first()

        if not product:
            raise Http404

        user.saves.remove(product)

        return Response({'success': True})