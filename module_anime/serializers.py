from django.db import transaction
from rest_framework import serializers

from module_anime.models import Anime, AnimeTitle


class AnimeTitleSerializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(queryset=Anime.objects)

    class Meta:
        model = AnimeTitle
        fields = [
            'id', 'title', 'language', 'anime'
        ]
        read_only_fields = ('created', 'updated')


class AnimeSerializer(serializers.ModelSerializer):
    anime_title = AnimeTitleSerializer(many=True, required=False)

    class Meta:
        model = Anime
        fields = [
            'id', 'api_id', 'anime_title', 'description', 'canonical_title',
            'average_rating', 'age_rating', 'status', 'episode_length',
            'nsfw', 'created_at', 'updated_at', 'favorite', 'user'
        ]
        read_only_fields = ('created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        anime_title_data = validated_data.pop('anime_title', None)
        instance = super().create(validated_data)
        # instance = Anime.objects.create(**validated_data)

        for anime_title in anime_title_data:
            anime_title['anime'] = instance
            AnimeTitle.objects.create(**anime_title)

        return instance
