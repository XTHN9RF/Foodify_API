from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from Foodify_API import views

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
