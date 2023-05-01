import datetime

from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.views import APIView

from Foodify_API import models
from Foodify_API import serializers
from Foodify_API import authentication


class RegistrationApiView(APIView):
    """Handle creating user accounts"""
    serializer_class = serializers.UserSerializer

    def post(self, request):
        """Create a new user"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = models.User.objects.get(email=request.data['email'])

            response = Response()

            access_token = authentication.create_access_token(user.id)
            refresh_token = authentication.create_refresh_token(user.id)

            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
            response.data = {
                'token': access_token,
                'message': 'User created successfully'
            }
            response.status_code = status.HTTP_201_CREATED
            return response

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


class CategoryApiView(APIView):
    """Handle getting and searching categories"""
    serializer_class = serializers.CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get(self, request):
        """Return a list of categories with search functionality provided"""
        is_token_valid = authentication.is_token_valid(request)

        if is_token_valid:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        return Response({'errorMessage': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        """Return a list of categories or searched categories"""
        queryset = models.Category.objects.all()
        category_name = self.request.query_params.get('search', None)
        if category_name:
            queryset = queryset.filter(slug__contains=category_name.lower())
        return queryset


class ProductsApiView(APIView):
    """Handle getting and searching products"""
    serializer_class = serializers.ProductSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get(self, request):
        """Gets a list of products with search functionality provided"""
        is_token_valid = authentication.is_token_valid(request)

        if is_token_valid:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        return Response({'errorMessage': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        """Return a list of all products or searched products"""
        queryset = models.Product.objects.all()
        product_name = self.request.query_params.get('search', None)
        category_name = self.request.query_params.get('category', None)
        if category_name:
            category_name = slugify(category_name)
            queryset = queryset.filter(category__slug=category_name)

        if product_name:
            queryset = queryset.filter(slug__contains=product_name.lower())
        return queryset


class SingleProductApiView(APIView):
    """Handle getting a single product"""
    serializer_class = serializers.ProductSerializer

    def get(self, request, pk=None):
        """Returns single product"""
        is_token_valid = authentication.is_token_valid(request)

        if is_token_valid:
            queryset = self.get_queryset()
            if not queryset:
                return Response({'errorMessage': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.ProductSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'errorMessage': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        """Returns single product by pk"""
        queryset = models.Product.objects.all()
        product_name = self.kwargs.get('pk', None)
        if product_name:
            product_name = slugify(product_name)
            queryset = queryset.filter(slug=product_name)
            return queryset
        else:
            return None


class CartApiView(APIView):
    """Handle getting and adding products to cart"""
    serializer_class = serializers.CartItemSerializer

    def get(self, request):
        """"Returns list of products that are in cart of current user"""
        is_token_valid = authentication.is_token_valid(request)

        if is_token_valid:
            user_id = authentication.decode_access_token(request)
            queryset = models.CartItem.objects.filter(user__id=user_id)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)

        return Response({'errorMessage': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        """Adds a product to cart"""
        is_token_valid = authentication.is_token_valid(request)

        if is_token_valid:
            user_id = authentication.decode_access_token(request)
            user = models.User.objects.get(id=user_id)
            product = models.Product.objects.get(slug=request.data['product_name'])
            quantity = request.data['quantity']
            cart_items = models.CartItem.objects.filter(user__id=user_id)

            for item in cart_items:
                if item.product == product:
                    item.quantity += quantity
                    item.save()
                    return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)

            new_cart_item = models.CartItem.objects.create(user=user, product=product, quantity=quantity)
            new_cart_item.save()
            return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)


class OrderApiView(APIView):
    """"Handle creating orders"""
    serializer_class = serializers.OrderSerializer

    def post(self, request):
        is_token_valid = authentication.is_token_valid(request)

        if is_token_valid:
            serializer = self.serializer_class(data=request.data)
            user_id = authentication.decode_access_token(request)
            user = models.User.objects.get(id=user_id)
            cart_items = models.CartItem.objects.filter(user__id=user_id)
            total_price = 0
            date = datetime.datetime.now()

            for item in cart_items:
                total_price += item.product.price * item.quantity

            if serializer.is_valid():
                receiver_street = serializer.validated_data['receiver_street']
                receiver_house_number = serializer.validated_data['receiver_house_number']
                receiver_phone_number = serializer.validated_data['receiver_phone_number']

                order = models.Order.objects.create(user=user, date=date,
                                                    receiver_street=receiver_street,
                                                    receiver_house_number=receiver_house_number,
                                                    receiver_phone_number=receiver_phone_number,
                                                    total_price=total_price)

                for item in cart_items:
                    order_item = models.OrderItem.objects.create(order=order, product=item.product,
                                                                 quantity=item.quantity)
                    order_item.save()

                order.save()
                cart_items.delete()

                return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'errorMessage': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
