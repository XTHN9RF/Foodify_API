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
    """Handle getting and searching categories"""
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = (permissions.IsReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = (permissions.IsReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        queryset = self.queryset.all()
        category_name = self.kwargs.get('pk')
        if category_name:
            queryset = queryset.filter(category__name=category_name)
        return queryset
