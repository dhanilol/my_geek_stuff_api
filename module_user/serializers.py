import binascii
import os

from django.contrib.auth import authenticate
from django.contrib.auth import password_validation as validators
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from django.db import transaction

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.settings import api_settings
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

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


class ApiKeyTokenSerializer(JSONWebTokenSerializer):
    def __init__(self, *args, **kwargs):
        super(ApiKeyTokenSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['api_key'] = PasswordField(write_only=True)

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'api_key': attrs.get('api_key')
        }

        if not all(credentials.values()):
            raise serializers.ValidationError('Authentication value missing')

        try:
            api_key = ApiKey.objects.get(
                key__exact=credentials['api_key'],
                user__username=credentials[self.username_field]
            )
        except Exception as e:
            raise serializers.ValidationError(e)

        if not api_key.user:
            raise serializers.ValidationError('Authentication Error')

        # TODO: move this to a separate utils file (update it to use from drf.jwt.utils)
        payload = jwt_payload_handler(api_key.user)
        payload['key_id'] = str(api_key.id)

        token = {
            'token': jwt_encode_handler(payload),
            'user': api_key.user
        }
        return token


class SignInSerializer(JSONWebTokenSerializer):
    def __init__(self, *args, **kwargs):
        super(SignInSerializer, self).__init__(*args, **kwargs)
        print('ASKJFGSHf')
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = api_settings.JWT_PAYLOAD_HANDLER(user)

                token = {
                    'token': api_settings.JWT_ENCODE_HANDLER(payload),
                    'user': user
                }

                return token

            else:
                msg = 'Cannot to log in with these credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username',
            'primary_email', 'primary_phone', 'password',
            'avatar'
        ]
