from django.conf.urls import include, url
from rest_framework import routers

from module_user.views.MeViewSet import MeViewset

router = routers.DefaultRouter()

router.register(r'me', MeViewset)

urlpatterns = [
    url(r'^', include(router.urls))
]