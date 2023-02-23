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

        query_params = {}

        if search_params.get('q'):
            query_params['q'] = urllib.parse.quote_plus(search_params.get('q'))

            if search_params.get('title'):
                query_params['q'] += "+intitle:{}".format(urllib.parse.quote_plus(search_params.get('title')))

            if search_params.get('author'):
                query_params['q'] += "+inauthor:{}".format(urllib.parse.quote_plus(search_params.get('author')))

            if search_params.get('publisher'):
                query_params['q'] += "+inpublisher:{}".format(urllib.parse.quote_plus(search_params.get('publisher')))

            # TODO: check if subject is the same as category
            if search_params.get('subject'):
                query_params['q'] += "+insubject:{}".format(urllib.parse.quote_plus(search_params.get('subject')))

            if search_params.get('isbn'):
                query_params['q'] += "+isbn:{}".format(urllib.parse.quote_plus(search_params.get('isbn')))

        if 'language' in search_params:
            query_params['langRestrict'] = urllib.parse.quote_plus(search_params.get('language'))
        # TODO: check all filter options on google api

        response = requests.get(url=endpoint, headers=self.header, params=query_params)
        if response.status_code == 200:
            return response.json()
        else:
            raise response.text

    def map_data(self, data) -> dict:
        volume_info = data['volumeInfo']

        try:
            mapped_data = {
                'api_book_id': volume_info.get('id'),
                'title': volume_info.get('title'),
                'author': self.__map_authors(volume_info.get('authors')),
                'description': volume_info.get('description'),
                'language': volume_info.get('language'),
                'average_rating': volume_info.get('averageRating'),
                'age_rating': volume_info.get('ageRating'),
                'page_count': volume_info.get('pageCount'),
                'published_at': volume_info.get('publishedDate'),
                'edition': volume_info.get('edition'),
                'publisher': self.__map_publisher(volume_info.get('publisher')),
                'category': self.__map_categories(volume_info.get('categories')),
                # 'industry_identifiers': volume_info.get['industryIdentifiers']
            }
            return mapped_data

        except Exception as e:
            raise e

    def __map_authors(self, authors):
        mapped_author = list()
        for author in authors:
            mapped_author.append({
                'name': author
            })
        return mapped_author

    def __map_categories(self, categories):
        mapped_categories = list()
        for category in categories:
            mapped_categories.append({
                'name': category,
                'description': ''
            })
        return mapped_categories

    def __map_publisher(self, publishers):
        mapped_publishers = list()
        if type(publishers) == str:
            return {
                'name': publishers,
                'description': ''
            }
        for publisher in publishers:
            mapped_publishers.append({
                'name': publisher,
                'description': ''
            })
        return mapped_publishers

    def availability(self, api_book_id):
        # TODO: search on google api where is available to buy/read
        pass
