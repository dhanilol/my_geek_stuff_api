import urllib.parse
import requests

from environ import environ

env = environ.Env()


def generate_headers():
    return {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }


class GoogleBooksApiHelper:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = env('GOOGLE_BOOKS_BASE_URL')
        self.token = None
        self.header = generate_headers()
        self.page_limit = 10

    def get(self, pk):
        endpoint = '{}/volumes/{}'.format(self.url, pk)

        response = requests.get(endpoint, self.header)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()

    def search(self, search_params: dict):
        endpoint = self.url + '/volumes?'

        if search_params.get('q'):
            endpoint += "q={}".format(urllib.parse.quote_plus(search_params.get('q')))
        else:
            endpoint += "q={}".format(urllib.parse.quote_plus(search_params.get('title')))

        if search_params.get('title'):
            endpoint += "+intitle:{}".format(urllib.parse.quote_plus(search_params.get('title')))

        if search_params.get('author'):
            endpoint += "+inauthor:{}".format(urllib.parse.quote_plus(search_params.get('author')))

        if search_params.get('publisher'):
            endpoint += "+inpublisher:{}".format(urllib.parse.quote_plus(search_params.get('publisher')))

        # TODO: check if subject is the same as category
        if search_params.get('subject'):
            endpoint += "+insubject:{}".format(urllib.parse.quote_plus(search_params.get('subject')))

        if search_params.get('isbn'):
            endpoint += "+isbn:{}".format(urllib.parse.quote_plus(search_params.get('isbn')))

        query_params = {}
        if 'language' in search_params:
            endpoint += "&langRestrict={}".format(urllib.parse.quote_plus(search_params.get('language')))
        # TODO: check all filter options on google api

        response = requests.get(endpoint, self.header)
        if response.status_code == 200:
            return response.json()
        else:
            raise response.json()

    @staticmethod
    def map_data(data) -> dict:
        volume_info = data['volumeInfo']

        try:
            mapped_data = {
                'api_book_id': volume_info['id'],
                'title': volume_info['title'],
                'author': volume_info['authors'],
                'description': volume_info['description'],
                'language': volume_info['language'],
                'average_rating': volume_info['averageRating'],
                'age_rating': volume_info[''],
                'page_count': volume_info['pageCount'],
                'published_at': volume_info['publishedDate'],
                'edition': volume_info[''],
                'publisher': volume_info['publisher'],
                'category': volume_info['categories'],
                # 'industry_identifiers': volume_info['industryIdentifiers']
            }
            return mapped_data

        except Exception as e:
            raise e

    def availability(self, api_book_id):
        # TODO: search on google api where is available to buy/read
        pass
