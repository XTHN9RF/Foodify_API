from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import get_authorization_header

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


class CategoryApiView(APIView):
    """Handle getting and searching categories"""
    serializer_class = serializers.CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get(self, request):
        """Return a list of all categories or one category by name"""
        header = get_authorization_header(request).split()

        if header and len(header) == 2:
            token = header[1].decode('utf-8')
        else:
            return Response({'errorMessage': 'No token provided'}, status=status.HTTP_401_UNAUTHORIZED)

        is_token_valid = authentication.is_token_valid(token)

        if is_token_valid:
            queryset = self.get_queryset()
            serializer = serializers.CategorySerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'errorMessage': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        """Return a list of all categories or one category by name"""
        queryset = models.Category.objects.all()
        category_name = self.request.query_params.get('search', None)
        if category_name:
            queryset = queryset.filter(slug__contains=category_name.lower())
        return queryset
