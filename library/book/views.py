from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm
from .models import Book


def is_admin(user: User) -> bool:
    if user.is_authenticated and user.is_staff:
        return True
    raise PermissionDenied


def book_list(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()

    search_title = request.GET.get("title", "").strip()
    search_author = request.GET.get("author", "").strip()

    if search_title:
        books = books.filter(name__icontains=search_title)
    if search_author:
        books = books.filter(authors__name__icontains=search_author)

    books = books.distinct()

    context = {
        "books": books,
        "search_title": search_title,
        "search_author": search_author,
    }
    return render(request, "book_list.html", context)


def book_detail(request: HttpRequest, id: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=id)
    return render(request, "book_detail.html", {"book": book})


@user_passes_test(is_admin)
def book_delete(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "GET":
        book = Book.get_by_id(id)
        if book:
            book.delete()
            messages.success(request, f"Book #{id} has been deleted.")
        else:
            messages.warning(request, f"Book #{id} does not exist.")
    return redirect("book:book_list")


@user_passes_test(is_admin)
def book_edit(request: HttpRequest, id: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book #{id} has been updated.")
            return redirect("book:book_detail", id=id)
    else:
        form = BookForm(instance=book)

    return render(request, "book_edit.html", {"book": book, "form": form})


@user_passes_test(is_admin)
def book_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book has been created.")
            return redirect("book:book_list")
    else:
        form = BookForm()

    return render(request, "book_create.html", {"form": form})
