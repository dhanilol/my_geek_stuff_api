from django.db import transaction
from rest_framework import serializers

from module_book.models import Book, Author, Category


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        category_data = validated_data.pop('category', None)

        instance = super(BookSerializer, self).create(validated_data)

        for author in author_data:
            data = {
                'name': author
            }
            Author.objects.create(**data)

        for category in category_data:
            data = {
                'name': category,
            }
            Category.objects.create(**data)

        return instance
