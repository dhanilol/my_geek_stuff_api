from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from module_anime.models import AnimeTitle, Anime
from module_anime.serializers import AnimeTitlesSerializer, AnimeSerializer
from module_kitsu_api.views.KitsuApiViewset import KitsuApiViewset


class AnimeTitleViewset(viewsets.ModelViewSet):
    queryset = AnimeTitle.objects.all()
    serializer_class = AnimeTitlesSerializer
    permission_classes = [IsAuthenticated]
    ordering = '-id'

    def get_queryset(self):
        q = self.queryset.filter(anime__user=self.request.user.pk)
        return q


class AnimeViewset(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [IsAuthenticated]
    ordering = '-id'

    def get_queryset(self):
        q = self.queryset.filter(user=self.request.user)
        return q

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
                'user': user.id,
            }
            if 'titles' in anime_attr:
                titles_list = []
                titles = anime_attr.pop('titles')
                for index, language in enumerate(titles):
                    _data = {
                        # 'anime': anime.data.get('id'),
                        'title': titles[language],
                        'language': language,
                    }
                    titles_list.append(_data)
                data['anime_title'] = titles_list

            anime = AnimeSerializer(data=data)

            if not anime.is_valid():
                return Response(anime.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                _anime = anime.save()

                # if 'titles' in anime_attr:
                #     for index, language in enumerate(anime_attr['titles']):
                #         _data = {
                #             'title': anime_attr['titles'][language],
                #             'language': language,
                #             'anime': anime.data.get('id'),
                #         }
                #         title = AnimeTitlesSerializer(data=_data)
                #         if title.is_valid():
                #             _title = title.save()
                #         else:
                #             errors = title.errors
                #             return Response(errors, status=status.HTTP_400_BAD_REQUEST)

                # return Response(_anime, status=status.HTTP_201_CREATED)

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
