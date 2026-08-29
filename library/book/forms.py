from author.models import Author
from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["name", "description", "count", "authors"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control border-start-0 ps-0",
                    "placeholder": "Enter book title",
                }
            ),
            "count": forms.NumberInput(
                attrs={
                    "class": "form-control border-start-0 ps-0",
                    "min": "0",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control form-control-glossy",
                    "rows": 5,
                    "placeholder": "Provide a summary for this collection index...",
                }
            ),
            "authors": forms.SelectMultiple(
                attrs={
                    "class": "form-select form-select-glossy",
                    "style": "min-height: 130px;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["authors"].queryset = Author.objects.all()
        self.fields["name"].required = True
        if not self.instance.pk:
            self.fields["count"].initial = 1

    def clean_count(self):
        count = self.cleaned_data["count"]
        if count < 0:
            raise forms.ValidationError("Stock count cannot be negative.")
        return count
