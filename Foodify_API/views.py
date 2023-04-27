from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from Foodify_API import models, serializers, permissions


class RegistrationApiView(APIView):
    """Handle creating user accounts"""
    serializer_class = serializers.UserSerializer

    def post(self, request):
        """Create a new user"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User created successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response({"errorMessage": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    """Handle getting and searching categories"""
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    """Return objects for the current authenticated user only"""
    permission_classes = (permissions.IsReadOnly, IsAuthenticated)

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

    def get_queryset(self):
        """Return one product by name or all products"""
        queryset = self.queryset.all()
        product_name = self.kwargs.get('pk')
        if product_name:
            queryset = queryset.filter(slug=product_name)
        return queryset
