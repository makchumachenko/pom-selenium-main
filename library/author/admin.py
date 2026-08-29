from django.contrib import admin
from .models import Author
from book.models import Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "list_books"]
    search_fields = ["id", "surname", "name", "patronymic"]
    list_filter = ["books"]
    readonly_fields = ["list_books"]

    @admin.display(description="Books")
    def list_books(self, obj):
        return ', '.join(str(book.name) for book in obj.books.all())