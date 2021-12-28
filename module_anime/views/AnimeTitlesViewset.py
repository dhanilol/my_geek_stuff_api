from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from module_anime.models.AnimeTitles import AnimeTitles
from module_anime.serializers.AnimeTitlesSerializer import AnimeTitlesSerializer


class AnimeTitlesViewset(viewsets.ModelViewSet):
    queryset = AnimeTitles.objects.all()
    serializer_class = AnimeTitlesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        q = self.queryset.filter(anime__user=self.request.user.pk)
        return q
