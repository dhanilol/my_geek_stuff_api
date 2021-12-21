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
    def get(self, request, pk):
        endpoint = '{}/anime/{}'.format(self.url, pk)
        # safe_endpoint = urllib.parse.quote_plus(endpoint)

        response = requests.get(endpoint, self.header)
        if response.status_code == 200:
            return response.json()
        else:
            raise response.json()

    @action(methods=['GET'], detail=False)
    def search(self, request, search_params):
        endpoint = self.url + '/anime'
        # safe_endpoint = urllib.parse.quote_plus(endpoint)
        # safe_params = urllib.parse.quote_plus()
        # q = {
        #     "filter['text']": search_params.get('title'),
        #     "page[limit]": 5
        # }

        # TODO: remove this temporary thingy
        title = search_params.get('title')
        endpoint += "?filter[text]={}".format(urllib.parse.quote_plus(title))

        response = requests.get(endpoint, self.header)
        if response.status_code == 200:
            return response.json()
        else:
            raise response.json()
