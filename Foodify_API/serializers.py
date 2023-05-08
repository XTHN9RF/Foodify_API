from rest_framework import serializers
import datetime
from . import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        """Class that regulates behavior of the serializer"""
        model = models.User
        fields = ('email', 'name', 'last_name', 'settlement', 'password')
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
            settlement=validated_data['settlement'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user password"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the categories object"""

    class Meta:
        """Class that regulates behavior of the category serializer"""
        model = models.Category
        fields = ('name', 'image_url')
        extra_kwargs = {
            'name': {'required': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the products object"""

    class Meta:
        """Class that regulates behavior of the product serializer"""
        model = models.Product
        fields = ('name', 'price', 'description', 'image_url')


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for the cart items object"""
    product_name = serializers.CharField(source='product.name', read_only=True, write_only=False)
    product_price = serializers.DecimalField(source='product.price', max_digits=5, decimal_places=2, read_only=True,
                                             write_only=False)
    product_image = serializers.CharField(source='product.image_url', read_only=True, write_only=False)

    class Meta:
        """Class that regulates behavior of the cart item serializer"""
        model = models.CartItem
        fields = ('product_name', 'product_price', 'product_image', 'quantity')


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for the orders object"""

    class Meta:
        """Class that regulates behavior of the order serializer"""
        model = models.Order
        fields = ('receiver_phone_number', 'receiver_street', 'receiver_house_number')


class GetOrderSerializer(serializers.ModelSerializer):
    """Serializer for the orders object"""
    receiver_name = serializers.CharField(source='user.name', read_only=True, write_only=False)
    receiver_last_name = serializers.CharField(source='user.last_name', read_only=True, write_only=False)
    receiver_email = serializers.CharField(source='user.email', read_only=True, write_only=False)
    receiver_phone_number = serializers.CharField(read_only=True, write_only=False)
    date = serializers.DateTimeField(read_only=True, write_only=False, format="%d.%m.%Y %H:%M")
    status = serializers.CharField(read_only=True, write_only=False)

    class Meta:
        """Class that regulates behavior of the order serializer"""
        model = models.Order
        fields = ('receiver_name', 'receiver_last_name', 'receiver_email', 'receiver_phone_number', 'date',
                  'status')


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the order history object"""
    product_name = serializers.CharField(source='product', read_only=True, write_only=False)
    product_image = serializers.CharField(source='product.image_url', read_only=True, write_only=False)
    product_price = serializers.DecimalField(source='product.price', max_digits=5, decimal_places=2, read_only=True, )

    class Meta:
        """Class that regulates behavior of the order history serializer"""
        model = models.OrderItem
        fields = ('product_name', 'product_image', 'product_price', 'quantity')
