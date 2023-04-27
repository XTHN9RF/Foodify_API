from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from Foodify_API import models
from Foodify_API import serializers
from Foodify_API import permissions
from Foodify_API import authentication


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


class LoginApiView(APIView):
    """Handle logging in user accounts"""

    def post(self, request):
        """Login a user by checking email and password and returning an access and refresh token"""
        user = models.User.objects.get(email=request.data['email'])

        if not user:
            return Response({'errorMessage': 'User with such email not found'}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(request.data['password']):
            return Response({'errorMessage': 'Wrong password'}, status=status.HTTP_403_FORBIDDEN)

        access_token = authentication.create_access_token(user.id)
        refresh_token = authentication.create_refresh_token(user.id)

        response = Response()
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        response.data = {
            'token': access_token,
            'message': 'User logged in successfully'
        }
        response.status_code = status.HTTP_200_OK
        return response


class RefreshApiView(APIView):
    """Handle refreshing access token"""
    def get(self, request):
        """Refresh access token by checking validity of refresh token and user data, then returns a new access token"""
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'errorMessage': 'No refresh token'}, status=status.HTTP_403_FORBIDDEN)

        user_id = authentication.decode_refresh_token(refresh_token)
        if not user_id:
            return Response({'errorMessage': 'Invalid refresh token'}, status=status.HTTP_403_FORBIDDEN)

        user = models.User.objects.get(id=user_id)
        if not user:
            return Response({'errorMessage': 'User not found'}, status=status.HTTP_403_FORBIDDEN)

        access_token = authentication.create_access_token(user.id)
        response = Response()
        response.data = {
            'token': access_token,
            'message': 'Access token refreshed successfully'
        }
        response.status_code = status.HTTP_200_OK
        return response


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
