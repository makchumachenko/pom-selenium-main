from django.urls import path

from . import api

app_name = "book"

urlpatterns = [
    path("<int:id>/", api.BookDetailsView.as_view(), name="book_detail"),
    path("", api.BookListView.as_view(), name="book_list"),
]
