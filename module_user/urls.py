from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from module_user.views import (
    MeViewset,
    SignUpViewset
)

router = routers.DefaultRouter()

router.register('me', MeViewset)
router.register('signup', SignUpViewset)


urlpatterns = [
    path(r'', include(router.urls)),
]
