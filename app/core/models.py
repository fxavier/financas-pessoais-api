from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

TYPE = (
    ('DEBIT', 'DebitO'),
    ('CREDIT', 'CreditO')
)

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    
class Category(models.Model):
    description = models.CharField(max_length=255)
    operation = models.CharField(max_length=50, choices=TYPE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, max_length=255)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.description
    
class Account(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.description
    
class Record(models.Model):
    record_type = models.CharField(max_length=50, choices=TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    record_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    note = models.TextField(max_length=500)
    
    def __str__(self):
        return self.record_type
    
    
