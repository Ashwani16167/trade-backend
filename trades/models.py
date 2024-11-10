import uuid
from django.db import models
from django.conf import settings

class Stock(models.Model):
    stock_code = models.CharField(max_length=20, unique=True)
    stock_name = models.CharField(max_length=100)
    stock_price = models.DecimalField(max_digits=10, decimal_places=2)

class Watchlist(models.Model):
    watchlist_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # unique ID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, emailID, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, emailID=emailID, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, emailID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, emailID, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    emailID = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    age = models.PositiveIntegerField()
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=1000000.00)  # Default balance

    REQUIRED_FIELDS = ['full_name', 'emailID', 'gender', 'age']
    USERNAME_FIELD = 'username'

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username
