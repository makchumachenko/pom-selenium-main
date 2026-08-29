from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer


class BookListView(APIView):
    def check_version(self, version: str) -> bool:
        return version == "v1"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get(self, request: Request, version: str) -> Response:
        if self.check_version(version):
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({"error": "Invalid version"}, status=HTTP_400_BAD_REQUEST)

    def post(self, request: Request, version: str) -> Response:
        if self.check_version(version):
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({"error": "Invalid version"}, status=HTTP_400_BAD_REQUEST)


class BookDetailsView(APIView):
    def check_version(self, version: str) -> bool:
        return version == "v1"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get(self, request: Request, id: int, version: str) -> Response:
        if self.check_version(version):
            book = get_object_or_404(Book, id=id)
            serializer = BookSerializer(book, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({"error": "Invalid version"}, status=HTTP_400_BAD_REQUEST)

    def put(self, request: Request, id: int, version: str) -> Response:
        if self.check_version(version):
            book = get_object_or_404(Book, id=id)
            serializer = BookSerializer(instance=book, data=request.data, many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)

        return Response({"error": "Invalid version"}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id: int, version: str) -> Response:
        if self.check_version(version):
            book = get_object_or_404(Book, id=id)
            book.delete()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response({"error": "Invalid version"}, status=HTTP_400_BAD_REQUEST)
