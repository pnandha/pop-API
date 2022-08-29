from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class CreateProductView(APIView):
    def post(self, request):
     serializer = ProductSerializer(data=request.data)
     serializer.is_valid(raise_exception=True)
     serializer.save()
     return Response(serializer.data)
