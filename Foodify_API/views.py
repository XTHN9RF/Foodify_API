from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from Foodify_API import models, serializers, permissions


class UserViewSet(viewsets.ModelViewSet):
    """Handle creating and updating users"""
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsOwnerOrReadOnly,)


class LoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = (permissions.IsReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)