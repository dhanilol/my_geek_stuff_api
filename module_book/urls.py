from django.conf.urls import include, url
from rest_framework_nested import routers
# from rest_framework import routers


from module_book.views import BookViewset

# router = routers.DefaultRouter()
router = routers.SimpleRouter()

router.register(r'book', BookViewset)
# router.register(r'book_author', AuthorViewset)

# anime_router = routers.NestedSimpleRouter(router, r'anime')
# anime_router.register(r'anime_title', AnimeTitleViewset, basename='anime-animetitle')


urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'', include(anime_router.urls)),
]
