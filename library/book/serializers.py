from author.models import Author
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=False, validators=[UniqueValidator(queryset=Book.objects.all())]
    )

    author_ids = serializers.PrimaryKeyRelatedField(
        source="authors",
        queryset=Author.objects.all(),
        many=True,
    )

    class Meta:
        model = Book

        fields = [
            "id",
            "name",
            "description",
            "count",
            "author_ids",
            "year_of_publication",
        ]
