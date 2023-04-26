from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    """Return objects for the current authenticated user only"""
    permission_classes = (permissions.IsReadOnly, IsAuthenticated)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """Return one category by name or all categories"""
        queryset = self.queryset.all()
        category_name = self.kwargs.get('pk')
        if category_name:
            queryset = queryset.filter(slug=category_name)
        return queryset


class ProductsViewSet(viewsets.ModelViewSet):
    """Handle getting and searching products"""
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    """Return objects for the current authenticated user only"""
    permission_classes = (IsAuthenticated, permissions.IsReadOnly)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """Return one product by name or all products"""
        queryset = self.queryset.all()
        product_name = self.kwargs.get('pk')
        if product_name:
            queryset = queryset.filter(slug=product_name)
        return queryset
