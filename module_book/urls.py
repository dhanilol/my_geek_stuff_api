from django.conf.urls import include
from django.urls import path

from rest_framework import routers as drf_routers
from rest_framework_nested import routers

from module_book.views import BookViewset

# Set endpoints as DRF pattern
drf_book_router = drf_routers.DefaultRouter()
drf_book_router.register(r'book', BookViewset)


# TODO: nested endpoints for /author/{id}/book/
# # Set endpoints as nested pattern
# # https://github.com/alanjds/drf-nested-routers for more info
# nested_router = routers.SimpleRouter()
# nested_router.register(r'author', AuthorViewset)

urlpatterns = [
    path(r'', include(drf_book_router.urls)),
]
