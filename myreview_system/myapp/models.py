


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    otp = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


# class User(AbstractBaseUser):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     otp = models.IntegerField(null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     objects = CustomUserManager()  # Assign the custom manager here

#     def __str__(self):
#         return self.username
