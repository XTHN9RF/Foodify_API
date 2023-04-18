from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    """Manager that helps to create user with validated credentials and hashed password"""

    def create_user(self, email, name, last_name, password=None):
        """Function that creates user"""
        if not email or not name or not last_name:
            raise ValueError('User must have correct credentials')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, last_name, password):
        """Function that creates admin user"""
        user = self.create_user(email, name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model that describes users in the system"""
    email = models.EmailField(max_length=30, unique=True, )
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=150, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name', 'password']

    def __str__(self):
        """" Return string representation of user to display it understandably in the admin panel """
        return self.email


class CategoryManager(models.Manager):
    def create_category(self, name):
        if not name:
            raise ValueError('Category must have correct name')

        category = self.model(name=name)
        category.save(using=self._db)

        return category


class Category(models.Model):
    """Database model that represents categories in the application"""
    name = models.CharField(max_length=30)

    objects = CategoryManager()

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """" Return string representation of category to display it understandably in the admin panel """
        return self.name


class ProductManager(models.Manager):
    """Manager that helps to create product with full credentials"""

    def create_product(self, name, description, price, category):
        """Function that creates product"""
        if not name or not description:
            raise ValueError('Product must have correct name and description')
        elif not price:
            raise ValueError('Product must have a price')
        elif not category:
            raise ValueError('Product must have a category')

        product = self.model(name=name, description=description, price=price, category=category)
        product.save(using=self._db)

        return product


class Product(models.Model):
    """ Database model that describes products in the system """
    name = models.CharField(max_length=45)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    objects = ProductManager()

    REQUIRED_FIELDS = ['name', 'description', 'price', 'category']

    def __str__(self):
        """" Return string representation of product to display it understandably in the admin panel """
        return self.name


class AddressManager(models.Manager):
    """Manager that helps to create address with full or partial credentials"""
    def create_address(self, user, settlement, street_name=None, building_number=None, ):
        """Function that creates address for user"""
        if not settlement or not user:
            raise ValueError('Address must have correct settlement and user')

        address = self.model(street_name=street_name, settlement=settlement, building_number=building_number, user=user)
        address.save(using=self._db)

        return address


class Address(models.Model):
    """Database model that represents addresses of the user"""
    street_name = models.CharField(max_length=100, blank=True)
    settlement = models.CharField(max_length=50)
    building_number = models.CharField(max_length=10, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = AddressManager()

    REQUIRED_FIELDS = ['settlement', 'user']

    def __str__(self):
        """Return string representation of address to display full address in the admin panel """
        return f"{self.street_name} {self.building_number}, {self.settlement}"


class CartItem(models.Model):
    """Database model that represents item in the cart"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    REQUIRED_FIELDS = ['product', 'quantity', 'user']


class Order(models.Model):
    """Database model for orders representation"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)

    REQUIRED_FIELDS = ['user', 'address', 'cart_items', 'date', 'status']
