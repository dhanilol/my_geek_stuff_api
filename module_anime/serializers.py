from rest_framework import serializers

from module_anime.models import Anime, AnimeTitle


class AnimeTitlesSerializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(many=False, queryset=Anime.objects)

    class Meta:
        model = AnimeTitle
        fields = '__all__'
        read_only_fields = ('created', 'updated')


class AnimeSerializer(serializers.ModelSerializer):
    anime_title = AnimeTitlesSerializer(read_only=False, many=True)

    class Meta:
        model = Anime
        # fields = [
        #     'id', 'api_id', 'anime_title', 'description', 'canonical_title', 'average_rating', 'age_rating', 'status',
        #     'episode_length', 'nsfw', 'created_at', 'updated_at', 'favorite', 'user'
        # ]
        fields = '__all__'
        read_only_fields = ('created', 'updated')

        def to_representation(self, instance):
            response = super().to_representation(instance)
            response['anime_title'] = AnimeTitlesSerializer(instance.child).data
            return response
