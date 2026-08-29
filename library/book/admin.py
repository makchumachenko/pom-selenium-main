from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "authors_list", "year_of_publication", "available_books"]
    search_fields = ["id", "name", "year_of_publication"]
    list_filter = ["id", "name", "authors"]

    @admin.display(description="Authors")
    def authors_list(self, obj):
        return ', '.join(str(author) for author in obj.authors.all())

    @admin.display(description="Available books")
    def available_books(self, obj):
        return obj.count - obj.orders.filter(end_at__isnull=True).count()