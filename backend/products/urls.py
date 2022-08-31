from django.contrib import admin
from django.urls import path, include
from .views import CreateCategoryView, CreateProductView, DeleteProductView, GetProductByUserIdView, GetProductsView

urlpatterns = [
    path('create_product', CreateProductView.as_view()),
    path('delete_products', DeleteProductView.as_view()),
    path('create_category', CreateCategoryView.as_view()),
    path('products_by_user', GetProductByUserIdView.as_view()),
    path('products', GetProductsView.as_view())
]
