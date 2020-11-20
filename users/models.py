from django.db import models

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_jwt.settings import api_settings
from users.utils import generate_access_token, generate_refresh_token


class UserManager(BaseUserManager):

    def create_user(self, full_name, phone, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')
        if full_name is None:
            raise TypeError('Users should have a full name')
        if phone is None:
            raise TypeError('Users should have a phone')
        user = self.model(username=username, email=self.normalize_email(email), full_name=full_name, phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        access_token = generate_access_token(self)
        refresh_token = generate_refresh_token(self)
        return {
            'refresh': refresh_token,
            'access': access_token
        }
