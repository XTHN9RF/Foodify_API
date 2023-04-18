from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from Foodify_API import views

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('', include(router.urls)),
]
