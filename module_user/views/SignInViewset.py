
from rest_framework_jwt.views import JSONWebTokenAPIView

from module_user.serializers.SignInSerializer import SignInSerializer


class SignInViewset(JSONWebTokenAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        return super(SignInViewset, self).post(request, *args, **kwargs)