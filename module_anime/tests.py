import pytest

from django import urls
from django.urls import reverse

from rest_framework import status


class TestAnime:

    @pytest.mark.authentication
    def test_without_authentication(self, api_client):
        response = api_client.get('/module_anime/anime/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail']
        assert response.data['detail'] == "Authentication credentials were not provided."

    @pytest.mark.authentication
    def test_with_wrong_authentication(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abcd')
        response = api_client.get('/module_anime/anime/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.authentication
    @pytest.mark.django_db
    def test_with_authentication(self, api_client_with_credentials):
        response = api_client_with_credentials.get('/module_anime/anime/')

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.authentication
    @pytest.mark.django_db
    def test_with_admin_authentication(self, api_client_with_admin_credentials):
        response = api_client_with_admin_credentials.get('/module_anime/anime/')

        assert response.status_code == status.HTTP_200_OK
