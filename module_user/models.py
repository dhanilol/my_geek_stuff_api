import uuid

from django.conf import settings
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
    status = models.CharField(max_length=32, null=False, default='created')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'primary_email'
    REQUIRED_FIELDS = []


class ApiKey(models.Model):
    class Meta:
        verbose_name_plural = "API Keys"
        ordering = ['-created']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=False, default='Default')
    key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        related_name="ApiKey",
        default=0
    )

    def __str__(self):
        return self.name
