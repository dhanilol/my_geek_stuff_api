from django.contrib.auth import authenticate
from rest_framework import serializers

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.settings import api_settings


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
                    msg = _('Cannot to log in with these credentials.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)