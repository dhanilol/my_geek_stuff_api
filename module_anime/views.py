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
    def include(self, request):
        """
        Includes anime/anime title using an ID from Kitsu API.
        """
        kitsu_api = KitstuApiHelper()

        # TODO: use the api_name to find the API being consumed on each register

        api_anime_id = self.request.data.get('api_anime_id', None)
        if not api_anime_id:
            raise ValidationError({'api_anime_id': ['Required field']})

        # TODO: Adds this filters/validations somewhere move convenient
        q = Anime.objects.filter(api_anime_id=api_anime_id)
        # TODO: think about a good way to make the include works with path/put
        if q.count() > 0 and request.method == 'POST':
            raise ValidationError({'api_anime_id': ['ID Already included']})

        try:
            results = kitsu_api.get(pk=api_anime_id)
            if 'errors' in results:
                return Response(results, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e

        mapped_data = kitsu_api.map_data(data=results)
        mapped_data['favorite'] = self.request.data.get('favorite', None)
        mapped_data['user'] = self.request.user.pk

        serializer = self.get_serializer(data=mapped_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def details(self, request):
        anime = self.get_object()
        kitsu_api = KitstuApiHelper()

        try:
            details = kitsu_api.get(pk=anime.api_anime_id)
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
