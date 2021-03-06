from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.views import JSONWebTokenAPIView

from module_user.models import User

from module_user.serializers import (
    MeSerializer,
    SignInSerializer,
    UserSerializer,
    ApiKeyTokenSerializer
)


class MeViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        q = self.queryset.filter(pk=self.request.user.pk)
        return q


class SignInViewset(JSONWebTokenAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        return super(SignInViewset, self).post(request, *args, **kwargs)


class SignUpViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class GetTokenFromApiKey(JSONWebTokenAPIView):
    serializer_class = ApiKeyTokenSerializer

    def post(self, request, *args, **kwargs):
        return super(GetTokenFromApiKey, self).post(request, *args, **kwargs)


class GetTokenFromUserAuth(JSONWebTokenAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        return super(GetTokenFromUserAuth, self).post(request, *args, **kwargs)


get_token_apikey = GetTokenFromApiKey.as_view()
get_token_auth = GetTokenFromUserAuth.as_view()
