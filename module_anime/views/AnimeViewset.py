from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from module_anime.models.Anime import Anime
from module_anime.serializers.AnimeSerializer import AnimeSerializer


class AnimeViewset(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [IsAuthenticated]  # TODO: change permissions to IsAuthenticated

    def get_queryset(self):
        q = self.queryset.filter(pk=self.request.user.pk)
        return q

    @action(methods=['GET'], detail=True)
    def details(self, request, pk):
        print(self.request)
        return Response(status=status.HTTP_200_OK)
