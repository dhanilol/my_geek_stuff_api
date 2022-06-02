from urllib.request import urlopen

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from libs.kitsu_api.KitsuApiHelper import KitstuApiHelper
from module_anime.models import Anime, AnimeTitle

from module_anime.serializers import AnimeSerializer, AnimeTitleSerializer


class AnimeViewset(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [BelongsToApiKey]
    ordering = '-id'

    def get_queryset(self):
        q = self.queryset.filter(user=self.request.user)
        return q

    @action(methods=['POST', 'PUT', 'PATCH'], detail=False)
    def include(self):
        """
        Includes anime/anime title using an ID from Kitsu API.
        """
        kitsu_api = KitstuApiHelper()

        anime_id = self.request.get('api_id', None)
        if not anime_id:
            raise ValidationError({'api_id'}, 'Required field')

        try:
            results = kitsu_api.get(pk=anime_id)
            if 'errors' in results:
                return Response(results, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e

        mapped_data = kitsu_api.map_data(data=results)
        mapped_data['user'] = self.request.user

        anime = AnimeSerializer(data=mapped_data)
        if not anime.is_valid():
            return Response(anime.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            _anime = anime.save()

        return Response(_anime, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def details(self, request):
        anime = self.get_object()
        kitsu_api = KitstuApiHelper()

        try:
            details = kitsu_api.get(pk=anime.api_id)
            if details:
                return Response(details, status=status.HTTP_200_OK)
            else:
                raise details
        except Exception as e:
            raise e

    @action(methods=['GET'], detail=False)
    def search(self, request, **kwargs):
        kitsu_api = KitstuApiHelper()

        results = kitsu_api.search(search_params=request.query_params)
        if results:
            return Response(results, status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        # TODO: handle request errors


class AnimeTitleViewset(viewsets.ModelViewSet):
    queryset = AnimeTitle.objects.all()
    serializer_class = AnimeTitleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        q = self.queryset.filter(anime__user=self.request.user.pk)
        return q
