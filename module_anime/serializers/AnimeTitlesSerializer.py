from rest_framework import serializers

from module_anime.models import Anime
from module_anime.models.AnimeTitles import AnimeTitles


class AnimeTitlesSerializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(many=False, queryset=Anime.objects)

    class Meta:
        model = AnimeTitles
        fields = [
            'id', 'title', 'language', 'anime'
        ]
        read_only_fields = ('created', 'updated')
