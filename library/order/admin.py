from django.contrib import admin
from django import forms
from .models import Order
from book.models import Book
from django.db.models import Count, F, Q


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "book" not in self.fields:
            return
        self.fields["book"].queryset = (
            Book.objects
            .annotate(
                active_orders=Count(
                    "orders",
                    filter=Q(orders__end_at__isnull=True),
                )
            )
            .filter(active_orders__lt=F("count"))
        )
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ["id", "str_user", "str_book", "created_at",
                    "planned_end_at", "end_at"]
    fieldsets = [
        (
            None,
            {
                "fields": ["user", "book", "planned_end_at"],
            },
        ),
        (
            "Actual return date",
            {
                "fields": ["end_at"],
            },
        ),
    ]

    @admin.display(description="User")
    def str_user(self, obj):
        return str(obj.user)

    @admin.display(description="Book")
    def str_book(self, obj):
        return str(obj.book)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ("book",)
        return ()