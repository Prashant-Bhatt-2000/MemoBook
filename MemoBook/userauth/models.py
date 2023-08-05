from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from uuid import uuid4

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.UUIDField(default=uuid4, primary_key=True, auto_created=True)
    name = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # Add any other required fields here
    # For example: 'name', 'is_active', etc.

    def __str__(self):
        return self.email



class Memo(models.Model): 
    id = models.UUIDField(default=uuid4, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    memo = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    day = models.TextField(default=timezone.now().day)
    is_completed = models.BooleanField(default=False)
