from django.urls import path

from . import api

app_name = "book"

urlpatterns = [
    path("<int:id>/", api.OrderDetailsView.as_view(), name="order_detail"),
    path("", api.OrderListView.as_view(), name="order_list"),
]
