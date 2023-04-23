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
    path('products/<str:pk>/', views.ProductsViewSet.as_view({'get': 'list'}), name='products-of-specific-category'),
    path('single-product/<str:pk>/', views.SingleProductViewSet.as_view({'get': 'list'}), name='single-product'),
    path('', include(router.urls)),
]
