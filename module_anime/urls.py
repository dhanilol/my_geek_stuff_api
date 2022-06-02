from django.conf.urls import include, url
from rest_framework_nested import routers
# from rest_framework import routers


from module_anime.views import AnimeViewset, AnimeTitleViewset

# router = routers.DefaultRouter()
router = routers.SimpleRouter()

router.register(r'anime', AnimeViewset)
router.register(r'anime_title', AnimeTitleViewset)

anime_router = routers.NestedSimpleRouter(router, r'anime')
anime_router.register(r'anime_title', AnimeTitleViewset, basename='anime-animetitle')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'', include(anime_router.urls)),
]
