from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from module_book.models import Book, Author, Category, Publisher


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


class BookIncludeRequestSerializer(serializers.Serializer):
    api_name = serializers.ChoiceField(choices=['google_books', 'nyt'], required=True)
    api_book_id = serializers.CharField(required=True)


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, required=False)
    category = BookCategorySerializer(many=True, required=False)
    publisher = PublisherSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        category_data = validated_data.pop('category', None)
        publisher_data = validated_data.pop('publisher', None)

        instance = super(BookSerializer, self).create(validated_data)

        for author in author_data:
            author['book'] = instance
            Author.objects.create(**author)

        for category in category_data:
            author['book'] = instance
            Category.objects.create(**category)

        for publisher in publisher_data:
            author['book'] = instance
            Publisher.objects.create(**publisher)

        return instance
