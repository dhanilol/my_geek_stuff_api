import binascii
import os

from django.contrib.auth import authenticate
from django.contrib.auth import password_validation as validators
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from django.db import transaction

from rest_framework import serializers
from rest_framework.fields import empty
# from rest_framework.settings import api_settings
# from rest_framework_jwt.settings import api_settings
# from rest_framework_jwt.compat import PasswordField
# from rest_framework_jwt.serializers import JSONWebTokenSerializer
# from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

from module_user.models import User, ApiKey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username',
            'primary_email', 'primary_phone', 'password',
            'avatar', 'status', 'created', 'updated'
        ]
        read_only_fields = ('status', 'created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        if 'password' in validated_data:
            new_password = make_password(validated_data['password'])
            validated_data['password'] = new_password

        return super(UserSerializer, self).create(validated_data)


class ApiKeySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'name', 'user', 'key', 'created', 'updated')
        read_only_fields = ('key', 'created', 'updated')
        model = ApiKey


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username',
            'primary_email', 'primary_phone', 'password',
            'avatar'
        ]
