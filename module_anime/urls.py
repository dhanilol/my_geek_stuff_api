from django.conf.urls import include, url
from rest_framework import routers

from module_anime.views.AnimeViewset import AnimeViewset
from module_anime.views.AnimeTitlesViewset import AnimeTitlesViewset

router = routers.DefaultRouter()

router.register(r'anime', AnimeViewset)
router.register(r'anime_titles', AnimeTitlesViewset)


urlpatterns = [
    url(r'^', include(router.urls)),
]
