"""DjangoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('documentation/schema/', SpectacularAPIView.as_view(), name='documentation'),
    path('documentation/', SpectacularRedocView.as_view(url_name='documentation'), name='redoc'),
    path('documentation/api/', SpectacularSwaggerView.as_view(url_name='documentation'), name='swagger-ui'),


    # TODO: set an application for auth & overwrite method
    path('auth/get_token/', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/refresh_token', TokenRefreshView.as_view(), name='token_refresh'),

    path(r'module_user/', include('module_user.urls')),
    path(r'module_anime/', include('module_anime.urls'))
]
