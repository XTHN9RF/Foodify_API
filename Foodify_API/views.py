from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from Foodify_API import models, serializers


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

