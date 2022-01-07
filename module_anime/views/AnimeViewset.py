from urllib.request import urlopen

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from module_anime.models.Anime import Anime
from module_anime.models.AnimeTitles import AnimeTitles
from module_anime.serializers.AnimeSerializer import AnimeSerializer
from module_anime.serializers.AnimeTitlesSerializer import AnimeTitlesSerializer
from module_kitsu_api.views.KitsuApiViewset import KitsuApiViewset


class AnimeViewset(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [IsAuthenticated]
    ordering = '-id'

    def get_queryset(self):
        q = self.queryset.filter(user=self.request.user)
        return q

    # TODO: if necessary, try using transaction
    @action(methods=['POST', 'PUT', 'PATCH'], detail=False)
    def include(self, request):
        """
        Includes anime/anime title using an ID from Kitsu API.
        """
        user = self.request.user
        kitsu_api = KitsuApiViewset()

        query_params = request.query_params
        if not query_params.get('api_id'):
            return Response("{'api_id': 'Not Found'}", status=status.HTTP_404_NOT_FOUND)

        try:
            results = kitsu_api.get(request=request, pk=query_params.get('api_id'))
        except Exception as e:
            raise e

        if 'errors' in results:
            return Response(results, status=status.HTTP_404_NOT_FOUND)
        else:
            # TODO: add to db based on kitsu api response
            anime_data = results['data']
            anime_attr = results['data']['attributes']

            # TODO: verify on DB if there's not added already for the same user
            # this works but maybe not the best
            # anime_attr['api_id'] = anime_data['id']
            # anime_attr['canonical_title'] = anime_attr['canonicalTitle']
            # anime_attr['user'] = user.id

            data = {
                'api_id': anime_data['id'],
                'description': anime_attr['description'],
                'canonical_title': anime_attr['canonicalTitle'],
                'average_rating': anime_attr['averageRating'],
                'age_rating': anime_attr['ageRating'],
                'status': anime_attr['status'],
                'episode_length': anime_attr['episodeLength'],
                'nsfw': anime_attr['nsfw'],
                'created_at': anime_attr['createdAt'],
                'updated_at': anime_attr['updatedAt'],
                'user': user.id
            }
            anime = AnimeSerializer(data=data)

            if not anime.is_valid():
                return Response(anime.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                _anime = anime.save()

                if 'titles' in anime_attr:
                    for index, language in enumerate(anime_attr['titles']):
                        _data = {
                            'title': anime_attr['titles'][language],
                            'language': language,
                            'anime': anime.data.get('id'),
                        }
                        title = AnimeTitlesSerializer(data=_data)
                        if title.is_valid():
                            _title = title.save()
                        else:
                            errors = title.errors
                            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(_anime, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def details(self, request, pk):
        anime = self.get_object()
        kitsuApi = KitsuApiViewset()

        details = kitsuApi.get(pk=anime.api_id)
        if details:
            return Response(details, status=status.HTTP_200_OK)
        else:
            # TODO: handle errors
            raise details

    @action(methods=['GET'], detail=False)
    def search(self, request, **kwargs):
        kitsu_api = KitsuApiViewset()
        # TODO: validate if valid params
        query_params = request.query_params

        results = kitsu_api.search(request=request, search_params=query_params)
        if results:
            return Response(results, status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        # TODO: handle request errors
