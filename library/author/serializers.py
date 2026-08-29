from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=False, validators=[UniqueValidator(queryset=Author.objects.all())]
    )
    
    class Meta:
        model = Author
        fields = ["id", "name", "surname", "patronymic"]
