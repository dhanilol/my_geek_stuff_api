from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from libs.book.google_books.GoogleBooksApiHelper import GoogleBooksApiHelper
from module_book.models import Book
from module_book.serializers import BookSerializer


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
        books_api = GoogleBooksApiHelper()

        # TODO: use the api_name to find the API being consumed on each register
        api_helper = self.__get_api_helper(request.get('api_name'))

        api_book_id = self.request.data.get('api_book_id', None)
        if not api_book_id:
            raise ValidationError({'api_book_id': ['Required field']})

        # # TODO: Adds this filters/validations somewhere move convenient
        # q = Book.objects.filter(api_book_id=api_book_id)
        # # TODO: think about a good way to make the include works with path/put
        # if q.count() > 0 and request.method == 'POST':
        #     raise ValidationError({'api_book_id': ['ID Already included']})

        try:
            results = books_api.get(pk=api_book_id)
            if 'errors' in results:
                return Response(results, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e

        # TODO: map data from API
        mapped_data = books_api.map_data(data=results)
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
        books_api = GoogleBooksApiHelper()

        results = books_api.search(search_params=request.query_params)
        if results:
            return Response(results, status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        # TODO: handle request errors


    def __get_api_helper(self, api_name):
        pass