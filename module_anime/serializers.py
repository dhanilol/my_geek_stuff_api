from django.db import transaction
from rest_framework import serializers

from module_anime.models import Anime, AnimeTitle


class AnimeTitleSerializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(many=False, queryset=Anime.objects, required=False)

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
            'id', 'api_anime_id', 'anime_title', 'description', 'canonical_title',
            'average_rating', 'age_rating', 'status', 'episode_length',
            'nsfw', 'created_at', 'updated_at', 'favorite', 'user'
        ]
        read_only_fields = ('created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        anime_title_data = validated_data.pop('anime_title', None)
        instance = super(AnimeSerializer, self).create(validated_data)

        for anime_title in anime_title_data:
            anime_title['anime'] = instance
            AnimeTitle.objects.create(**anime_title)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        anime_title_data = validated_data.pop('anime_title', None)
        instance = super(AnimeSerializer, self).update(instance=instance, validated_data=validated_data)

        if anime_title_data and anime_title_data != instance.anime_title:
            # Since no custom data is stored here. We delete all and add it again
            anime_titles = AnimeTitle.objects.get(anime=instance.pk)
            anime_titles.delete()

            for anime_title in anime_title_data:
                anime_title['anime'] = instance
                AnimeTitle.objects.create(**anime_title)

        return instance

