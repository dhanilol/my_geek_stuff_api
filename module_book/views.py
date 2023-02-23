from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from libs.book.google_books.GoogleBooksApiHelper import GoogleBooksApiHelper
from module_book.models import Book
from module_book.serializers import BookSerializer, BookIncludeRequestSerializer


class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [BelongsToApiKey]
    ordering = '-id'

    def get_queryset(self):
        q = self.queryset.filter(user=self.request.user)
        return q

    @action(methods=['POST', 'PUT', 'PATCH'], detail=False)
    def include(self, request):
        """
        Includes books using an ID from External API.
        """
        request_serializer = BookIncludeRequestSerializer(data=self.request.data)
        request_serializer.is_valid(raise_exception=True)

        api_helper = self.__get_api_helper(self.request.data.get('api_name'))
        api_book_id = self.request.data.get('api_book_id', None)

        self.__validate_duplicated_data(api_book_id)

        try:
            results = api_helper.get(pk=api_book_id)
            if 'errors' in results:
                return Response(results, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e

        # TODO: map data from API
        mapped_data = api_helper.map_data(data=results)
        mapped_data['favorite'] = self.request.data.get('favorite', None)
        mapped_data['user'] = self.request.user.pk

        serializer = self.get_serializer(data=mapped_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def details(self, request):
        book = self.get_object()
        books_api = GoogleBooksApiHelper()

        try:
            details = books_api.get(pk=book.api_book_id)
            if details:
                return Response(details, status=status.HTTP_200_OK)
            else:
                raise details
        except Exception as e:
            raise e

    @action(methods=['GET'], detail=False)
    def search(self, request, **kwargs):
        if 'q' not in request.query_params:
            raise ValidationError({'q': ['Required field']})

        books_api = GoogleBooksApiHelper()

        results = books_api.search(search_params=request.query_params)
        if results:
            return Response(results, status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        # TODO: handle request errors

    def __get_api_helper(self, api_name: str):
        return {
            'google_books': GoogleBooksApiHelper()
        }.get(api_name)

    def __validate_duplicated_data(self, api_id):
        q = self.queryset.filter(api_book_id=api_id, user__id=self.request.user.pk)
        if q.count() > 0:
            raise ValidationError({'api_book_id': ['ID Already included']})
