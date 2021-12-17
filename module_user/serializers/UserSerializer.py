from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from module_user.models.User import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username', 'primary_email', 'primary_phone', 'password', 'avatar',
            'status', 'created', 'updated'
        ]
        read_only_fields = ('status', 'created', 'updated')

    def create(self, validated_data):
        if 'password' in validated_data:
            new_password = make_password(validated_data['password'])
            validated_data['password'] = new_password

        user = super(UserSerializer, self).create(validated_data)
        return user
