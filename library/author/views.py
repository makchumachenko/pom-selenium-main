from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from rest_framework import permissions, viewsets

from . import serializers
from .forms import AuthorForm
from .models import Author

User = get_user_model()


def is_admin(user) -> bool:
    if user.is_staff:
        return True
    raise PermissionDenied


@user_passes_test(is_admin)
def author_list(request: HttpRequest) -> HttpResponse:
    authors = Author.objects.all()
    form = AuthorForm()
    return render(
        request, "author/author_list.html", {"form": form, "authors": authors}
    )


@user_passes_test(is_admin)
def author_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Author added successfully!")
            return redirect("author:list")
        messages.error(request, "Invalid creation data")

    return author_list(request)


@user_passes_test(is_admin)
def author_delete(request: HttpRequest, id: int) -> HttpResponse:
    author = Author.objects.get(pk=id)
    if author.books.count() != 0:
        messages.error(request, "Delete the author's books first")
    else:
        author.delete()
    return author_list(request)


# @user_passes_test(is_admin)
# def author_books(request: HttpRequest, id: int) -> HttpResponse:
#     return render(request, "books/book_list", {"search_author": id})


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("id")
    serializer_class = serializers.AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]