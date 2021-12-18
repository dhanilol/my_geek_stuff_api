from django.db import models

from module_anime.models.Anime import Anime


class AnimeTitles(models.Model):
    id = models.AutoField(primary_key=True, max_length=10)
    title = models.CharField(max_length=255, null=False)
    language = models.CharField(max_length=16, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='anime')
