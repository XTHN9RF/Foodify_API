from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from Foodify_API import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductsViewSet)

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('products/<slug:pk>/', views.ProductsViewSet.as_view({'get': 'list'}), name='single-product'),
    path('categories/<slug:pk>/', views.CategoryViewSet.as_view({'get': 'list'}), name='products-of-specific-category'),
    path('', include(router.urls)),
]
