from django.conf.urls import include, url
from rest_framework import routers

from module_anime.views.AnimeViewset import AnimeViewset

router = routers.DefaultRouter()

router.register(r'anime', AnimeViewset)


urlpatterns = [
    url(r'^', include(router.urls)),
]
