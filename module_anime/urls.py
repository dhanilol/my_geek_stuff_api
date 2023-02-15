from django.conf.urls import include
from django.urls import path

from rest_framework_nested import routers
from rest_framework import routers as drf_routers

from module_anime.views import AnimeViewset, AnimeTitleViewset

# Set endpoints as DRF pattern
drf_router = drf_routers.DefaultRouter()
drf_router.register(r'anime', AnimeViewset)
drf_router.register(r'anime_title', AnimeTitleViewset)

# Set endpoints as nested pattern
# https://github.com/alanjds/drf-nested-routers for more info
nested_router = routers.SimpleRouter()

nested_router.register(r'anime', AnimeViewset)
nested_router.register(r'anime_title', AnimeTitleViewset)

anime_router = routers.NestedSimpleRouter(nested_router, r'anime')
anime_router.register(r'anime_title', AnimeTitleViewset, basename='anime-animetitle')


urlpatterns = [
    path(r'', include(nested_router.urls)),
    path(r'', include(drf_router.urls)),
    path(r'', include(anime_router.urls)),
]
