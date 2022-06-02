from django.db import transaction
from rest_framework import serializers

from module_anime.models import Anime, AnimeTitle


class AnimeSerializer(serializers.ModelSerializer):
    # anime_title = serializers.StringRelatedField(many=True)
    # anime_title = serializers.PrimaryKeyRelatedField(queryset=AnimeTitle.objects, required=False)

    class Meta:
        model = Anime
        fields = [
            'id', 'api_id', 'titles', 'description', 'canonical_title',
            'average_rating', 'age_rating', 'status', 'episode_length',
            'nsfw', 'created_at', 'updated_at', 'favorite', 'user'
        ]
        read_only_fields = ('created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        anime_title = validated_data.pop('anime_title', None)
        instance = super().create(validated_data=validated_data)

        if anime_title:
            self.__create_related(anime_title)

        return instance

    def __create_related(self, anime_title):
        for title in anime_title:
            title['anime'] = self.instance
            AnimeTitle.objects.create(**title)


class AnimeTitleSerializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(queryset=Anime.objects)

    class Meta:
        model = AnimeTitle
        fields = [
            'id', 'title', 'language', 'anime'
        ]
        read_only_fields = ('created', 'updated')