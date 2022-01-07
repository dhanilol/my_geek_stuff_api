from django.conf.urls import include, url
from rest_framework import routers

from module_user.views.MeViewSet import MeViewset
from module_user.views.SignInViewset import SignInViewset
from module_user.views.SignUpViewset import SignUpViewset

router = routers.DefaultRouter()

router.register(r'me', MeViewset)
router.register(r'signup', SignUpViewset)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'signin', SignInViewset.as_view())
]
