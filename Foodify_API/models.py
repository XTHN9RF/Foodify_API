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
        """" Return string representation of our user to display it understandably in the admin panel """
        return self.email


class Category(models.Model):
    """Database model that describes categories in the system"""
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        """" Return string representation of category to display it understandably in the admin panel """
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['name', 'description', 'price', 'category']

    def __str__(self):
        return self.name