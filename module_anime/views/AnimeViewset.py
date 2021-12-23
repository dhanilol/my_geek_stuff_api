from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from module_anime.models.Anime import Anime
from module_anime.serializers.AnimeSerializer import AnimeSerializer
from module_kitsu_api.views.KitsuApiViewset import KitsuApiViewset


class AnimeViewset(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [IsAuthenticated]  # TODO: change permissions to IsAuthenticated

    def get_queryset(self):
        q = self.queryset.filter(pk=self.request.user.pk)
        return q

    @action(methods=['POST', 'PUT', 'PATCH'], detail=False)
    def include(self, request):
        """
        Includes anime/anime title using an ID from Kitsu API.
        """
        kitsu_api = KitsuApiViewset()

        query_params = request.query_params
        if not query_params.get('api_id'):
            return Response("{'api_id': 'Not Found'}", status=status.HTTP_404_NOT_FOUND)

        try:
            results = kitsu_api.get(request=request, pk=query_params.get('api_id'))
        except Exception as e:
            raise e

        if not results:
            return Response(results, status=status.HTTP_404_NOT_FOUND)
        else:
            # TODO: add to db based on kitsu api response

            anime_serializer = AnimeSerializer(results)
            if not anime_serializer.is_valid():
                return Response(anime_serializer.errors)
            else:
                try:
                    anime_serializer.save()
                except Exception as e:
                    raise e

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
