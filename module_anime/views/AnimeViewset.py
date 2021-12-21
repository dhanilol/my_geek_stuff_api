from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
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
        query_params = request.query_params
        # TODO: validate if is a valid param
        # TODO: add multiple optional params
        params = {
            'title': query_params.get('title')
        }
        kitsuApi = KitsuApiViewset()

        results = kitsuApi.search(request=request, search_params=params)
        if results:
            return Response(results, status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
