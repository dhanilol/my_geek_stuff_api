from rest_framework import serializers

from module_anime.models.Anime import Anime


class AnimeSerializer(serializers.ModelSerializer):
    # titles = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='anime-titles-detail')

    class Meta:
        model = Anime
        fields = [
            'id', 'api_id', 'description', 'canonical_title', 'average_rating', 'age_rating', 'status', 'episode_length',
            'nsfw', 'created_at', 'updated_at', 'favorite', 'user'
        ]
        read_only_fields = ('created', 'updated')
