from django import forms

from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "surname", "patronymic"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control text-center", "placeholder": "Last Name"}
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control text-center", "placeholder": "First Name"}
            ),
            "patronymic": forms.TextInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "Middle Name",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["surname"].required = True
