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

from module_user.models import User, ApiKey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = [
        #     'id', 'first_name', 'last_name', 'username',
        #     'primary_email', 'primary_phone', 'password',
        #     'avatar', 'status', 'created', 'updated'
        # ]
        fields = '__all__'
        read_only_fields = ('status', 'created', 'updated')

    def __init__(self, instance=None, data=empty, **kwargs):
        super(UserSerializer, self).__init__(instance, data, **kwargs)

    @property
    def api_key(self):
        return self.ApiKey

    def validate(self, data):
        user = User(data)
        password = data.get('password', None)

        errors = dict()
        if password:
            try:
                validators.validate_password(password=password, user=user)
            except exceptions.ValidationError as ex:
                errors['password'] = list(ex.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return data
        # return super(UserSerializer, self).validated_data()

    @transaction.atomic
    def create(self, validated_data):
        if 'password' in validated_data:
            new_password = make_password(validated_data['password'])
            validated_data['password'] = new_password

        user = super(UserSerializer, self).create(validated_data)
        if user:
            apiKey = self.api_key.create()
        return user


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


class SignInSerializer(JSONWebTokenSerializer):
    def __init__(self, *args, **kwargs):
        super(SignInSerializer, self).__init__(*args, **kwargs)

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
