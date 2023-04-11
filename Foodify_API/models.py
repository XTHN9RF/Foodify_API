from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    """Database model that describes users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name', 'password']

    def __str__(self):
        """" Return string representation of user to display it understandably in the admin panel """
        return self.email


class Category(models.Model):
    """Database model that represents categories in the application"""
    name = models.CharField(max_length=255)

    def __str__(self):
        """" Return string representation of category to display it understandably in the admin panel """
        return self.name


class Product(models.Model):
    """ Database model that describes products in the system """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['name', 'description', 'price', 'category']

    def __str__(self):
        """" Return string representation of product to display it understandably in the admin panel """
        return self.name


class Address(models.Model):
    """Database model that represents addresses of the user"""
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    building_number = models.DecimalField(max_length=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['street', 'city', 'building_number', 'user']

    def __str__(self):
        """Return string representation of address to display full address in the admin panel """
        return f"{self.street_name} {self.building_number}, {self.city}"


class CartItem(models.Model):
    """Database model that represents item in the cart"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    REQUIRED_FIELDS = ['product', 'quantity', 'user']


class Order(models.Model):
    """Database model for orders representation"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=255)

    REQUIRED_FIELDS = ['user', 'address', 'cart_items', 'date', 'status']
