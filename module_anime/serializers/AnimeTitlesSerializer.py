from rest_framework import serializers

from module_anime.models.AnimeTitles import AnimeTitles


class AnimeTitlesSerializer(serializers.ModelSerializer):
    anime = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='anime-detail')

    class Meta:
        model = AnimeTitles
        fields = [
            'id', 'title', 'language', 'anime'
        ]
        read_only_fields = ('created', 'updated')
