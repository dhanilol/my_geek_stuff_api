from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True, max_length=10)
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=32, null=False, unique=True)
    primary_email = models.EmailField(max_length=255, null=False, unique=True)
    primary_phone = models.CharField(max_length=64, null=True, blank=True, default=None)
    password = models.CharField(max_length=255, null=False)
    avatar = models.TextField(null=True, blank=True, default=None)
    status = models.CharField(max_length=32, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'primary_email'
    REQUIRED_FIELDS = []
