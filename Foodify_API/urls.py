from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from Foodify_API import views


urlpatterns = [
    path('register', views.RegistrationApiView.as_view(), name='register'),
    path('login', views.LoginApiView.as_view(), name='login'),
    path('refresh', views.RefreshApiView.as_view(), name='refresh'),
    path('categories/', views.CategoryApiView.as_view(), name='categories'),
    path('products/', views.ProductsApiView.as_view(), name='products'),
    path('products/<slug:pk>', views.SingleProductApiView.as_view(), name='product'),
    path('cart/', views.CartApiView.as_view(), name='cart'),
]
