import urllib.parse
import requests

from environ import environ
from rest_framework import viewsets
from rest_framework.decorators import action

env = environ.Env()


def generate_headers():
    return {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }


class KitsuApiViewset(viewsets.GenericViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = env('KITSU_BASE_URL')
        self.token = None
        self.header = generate_headers()
        self.page_limit = 5

    @action(methods=['GET'], detail=True)
    def get_anime(self, request, pk):
        endpoint = self.url + '/anime/' + pk
        safe_endpoint = urllib.parse.quote_plus(endpoint)

        response = requests.get(safe_endpoint, self.header)
        if response.status_code == 200:
            return response.json()
        else:
            raise response.json()

    def search(self, request, params):
        endpoint = self.url + '/anime'
        # safe_endpoint = urllib.parse.quote_plus(endpoint)
        response = requests.get(endpoint, self.header, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise response.json()