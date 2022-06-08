from django.db import models

from module_user.models import User


class Anime(models.Model):
    id = models.AutoField(primary_key=True, max_length=10)
    api_id = models.IntegerField(max_length=10, null=False)

    description = models.TextField(null=True)
    canonical_title = models.CharField(max_length=255, null=False)
    average_rating = models.CharField(max_length=16, null=True)
    age_rating = models.CharField(max_length=16, null=True, blank=True)
    status = models.CharField(max_length=64, null=False)
    episode_length = models.PositiveIntegerField(null=True, blank=True, default=None)
    nsfw = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    favorite = models.BooleanField(null=False, default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='anime')


class AnimeTitle(models.Model):
    id = models.AutoField(primary_key=True, max_length=10)
    title = models.CharField(max_length=255, null=False)
    language = models.CharField(max_length=16, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='anime_title')

    # def __str__(self):
    #     return '%s: %s' % (self.language, self.title)


class AnimeAvailability(models.Model):
    id = models.AutoField(primary_key=True, max_length=10)
    streaming_service = models.CharField(max_length=255, null=False)
    seasons = models.IntegerField(max_length=8, null=True, default=None)

    anime = models.OneToOneField(Anime, on_delete=models.CASCADE, related_name='availability')
