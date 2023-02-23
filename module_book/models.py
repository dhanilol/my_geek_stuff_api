from django.db import models

from module_user.models import User


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    language = models.CharField(max_length=16, null=True)
    average_rating = models.CharField(max_length=16, null=True)
    age_rating = models.CharField(max_length=16, null=True, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True, default=None)
    published_at = models.DateTimeField(auto_now_add=True)
    edition = models.CharField(max_length=16, null=True)
    favorite = models.BooleanField(null=False, default=False)
    user_rating = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    api_book_id = models.IntegerField(
        null=True,
        verbose_name='The external API register ID for the register included'
    )

    api_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name='The external API name that for the register included',
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='book')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='book')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book')


# class BookAvailability(models.Model):
#     id = models.AutoField(primary_key=True, max_length=10)
#     reading_service = models.CharField(max_length=255, null=False)
#
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='availability')
