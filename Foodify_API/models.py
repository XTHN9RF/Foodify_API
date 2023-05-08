from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify


class UserManager(BaseUserManager):
    """Manager that helps to create user with validated credentials and hashed password"""

    def create_user(self, email, name, last_name, settlement, password=None):
        """Function that creates user"""
        if not email or not name or not last_name:
            raise ValueError('User must have correct credentials')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, last_name=last_name, settlement=settlement)
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
    settlement = models.CharField(max_length=50, blank=True)
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
    def create_category(self, name, image_url, slug=None):
        if not name:
            raise ValueError('Category must have correct name')
        if slug is None:
            slug = slugify(name)

        category = self.model(name=name, image_url=image_url, slug=slug)
        category.save(using=self._db)

        return category


class Category(models.Model):
    """Database model that represents categories in the application"""
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image_url = models.CharField(max_length=250, blank=True)

    objects = CategoryManager()

    REQUIRED_FIELDS = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        """" Return string representation of category to display it understandably in the admin panel """
        return self.name


class ProductManager(models.Manager):
    """Manager that helps to create product with full credentials"""

    def create_product(self, name, description, price, category, image_url, slug=None):
        """Function that creates product"""
        if not name or not description:
            raise ValueError('Product must have correct name and description')
        elif not price:
            raise ValueError('Product must have a price')
        elif not category:
            raise ValueError('Product must have a category')

        product = self.model(name=name, description=description, price=price, category=category, image_url=image_url,
                             slug=slug)
        product.save(using=self._db)

        return product


class Product(models.Model):
    """ Database model that describes products in the system """
    name = models.CharField(max_length=45, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=250, blank=True)

    objects = ProductManager()

    REQUIRED_FIELDS = ['name', 'description', 'price', 'category']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        """" Return string representation of product to display it understandably in the admin panel """
        return self.name


class CartItem(models.Model):
    """Database model that represents item in the cart"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    REQUIRED_FIELDS = ['product', 'quantity', 'user']


class Order(models.Model):
    """Database model for orders representation"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    receiver_street = models.CharField(max_length=50, blank=True, null=True)
    receiver_house_number = models.CharField(max_length=10, blank=True, null=True)
    receiver_phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='Processing')

    REQUIRED_FIELDS = ['user', 'cart_items', 'date', 'status', 'total_price', 'receiver_phone_number',
                       'receiver_street', 'receiver_house_number']


class OrderItem(models.Model):
    """Database model that represents item in the order"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['product', 'quantity', 'order']
