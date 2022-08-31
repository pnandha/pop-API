from http.client import NOT_ACCEPTABLE
from sre_constants import SUCCESS
from unicodedata import category, name
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotAcceptable
import jwt
from django.db.models import Q                          
from django.conf import settings
from products.models import Products
from users.models import User

from users.serializers import UserSerializer
from .serializers import ProductSerializer, CategorySerializer


# Create your views here.
class CreateProductView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=uuid.UUID(payload['id'])).first()

    
    
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DeleteProductView(APIView):
    def delete(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=uuid.UUID(payload['id'])).first()

        products = Products.objects.all()

        products = products.filter(id=request.body['id'], many=True)
        products.delete()

        return Response({
            "message": "SUCCESS"
        })

class CreateCategoryView(APIView):
    def post(self, request):
          token = request.COOKIES.get('jwt')

          if not token:
            raise AuthenticationFailed('Unauthenticated') 

          try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

          except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

          serializer = CategorySerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data)


class GetProductByUserIdView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        
        product = Products.objects.filter(user_id_id=uuid.UUID(payload['id']))
        serializer = ProductSerializer(product ,many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

class GetProductsView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated') 

        try: 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        search = request.GET.get('search')
        tradingFor = request.GET.get('tradingfor')
        categoryid = request.GET.get('categoryid')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 10))
        products = Products.objects.all()

        if search:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        if tradingFor:
            products = products.filter(trading_for__icontains=tradingFor)

        if categoryid:
            products = products.filter(category=categoryid)

        start = (page - 1) * page_size
        end = page * page_size
        total_products = products.count()
        serializer = ProductSerializer(products[start : end] ,many=True)
        return Response(
            {
            "page":  page,
            "page_size": page_size,
            "content": serializer.data,
            "product_total": total_products,
            }
        )





     
