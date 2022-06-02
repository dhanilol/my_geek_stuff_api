import urllib.parse
import requests

from environ import environ

env = environ.Env()


def generate_headers():
    return {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }


class KitstuApiHelper:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = env('KITSU_BASE_URL')
        self.token = None
        self.header = generate_headers()
        self.page_limit = 10

    def get(self, pk):
        endpoint = '{}/anime/{}'.format(self.url, pk)

        response = requests.get(endpoint, self.header)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()

    def search(self, search_params={}):
        endpoint = self.url + '/anime?'

        if search_params.get('title'):
            endpoint += "filter[text]={}".format(urllib.parse.quote_plus(search_params.get('title')))

        if search_params.get('category'):
            endpoint += "&filter[categories]={}".format(urllib.parse.quote_plus(search_params.get('category')))

        endpoint += "&page[limit]={}".format(self.page_limit)

        response = requests.get(endpoint, self.header)
        if response.status_code == 200:
            return response.json()
        else:
            raise response.json()
