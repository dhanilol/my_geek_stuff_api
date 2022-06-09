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

    def map_data(self, data) -> dict:
        try:
            anime_data = data['data']
            anime_attr = anime_data['attributes']

            mapped_data = {
                'api_anime_id': anime_data['id'],
                'description': anime_attr['description'],
                'canonical_title': anime_attr['canonicalTitle'],
                'average_rating': anime_attr['averageRating'],
                'age_rating': anime_attr['ageRating'],
                'status': anime_attr['status'],
                'episode_length': anime_attr['episodeLength'],
                'nsfw': anime_attr['nsfw'],
                'created_at': anime_attr['createdAt'],
                'updated_at': anime_attr['updatedAt'],
            }

            if 'titles' in anime_attr:
                anime_titles = [
                    {'title': anime_attr['titles'][language], 'language': language}
                    for index, language in enumerate(anime_attr['titles'])
                ]
                mapped_data['anime_title'] = anime_titles

            return mapped_data

        except Exception as e:
            raise e
