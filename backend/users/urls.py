from django.contrib import admin
from django.urls import path, include
from .views import LogoutView, RegisterView, LoginView, UserView, UserInfoView, SaveProdView, UnsaveProductView, UpdateUserView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('update', UpdateUserView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user/info', UserInfoView.as_view()),
    path('save', SaveProdView.as_view()),
    path('unsave', UnsaveProductView.as_view())
]
