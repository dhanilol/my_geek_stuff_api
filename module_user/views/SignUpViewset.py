from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from module_user.models.User import User

from module_user.serializers.UserSerializer import UserSerializer


class SignupViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
