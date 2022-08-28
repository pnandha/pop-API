from multiprocessing import AuthenticationError
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

from .models import User

from .serializers import UserSerializer

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
     serializer = UserSerializer(data=request.data)
     serializer.is_valid(raise_exception=True)
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
        
        return Response(
            {'message': 'success'}
            )
