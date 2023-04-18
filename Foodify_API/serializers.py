from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        """Class that regulates behavior of the serializer"""
        model = models.User
        fields = ('id', 'email', 'name', 'last_name', 'password')
        extra_kwargs = {'password': {
            'write_only': True,
            'read_only': False,
            'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = models.User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user password"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
