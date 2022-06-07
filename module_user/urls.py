from django.conf.urls import include, url
from rest_framework import routers

from module_user.views import (
    MeViewset,
    SignUpViewset,
    SignInViewset,
    get_token_apikey,
    get_token_auth
)

router = routers.DefaultRouter()

router.register(r'me', MeViewset)
router.register(r'signup', SignUpViewset)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'signin', SignInViewset.as_view()),
    url(r'auth/get_token', get_token_apikey),
    url(r'auth/auth_token', get_token_auth),
]
