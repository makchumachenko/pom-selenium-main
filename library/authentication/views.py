from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from . import forms

User = get_user_model()


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")

            form.add_error(None, "Invalid email or password.")
    else:
        form = forms.LoginForm()

    return render(request, "authentication/login.html", {"form": form})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            cleaned = form.cleaned_data.copy()
            email = cleaned.pop("email")
            password = cleaned.pop("password")

            try:
                new_user = User.objects.create_user(email, password, **cleaned)
                login(request, new_user)
                messages.success(request, f"Logged in as {email}")
                return redirect("home")
            
            except ValidationError as e:
                for field, errors in e.error_dict.items():
                    for error in errors:
                        form.add_error(field, error)

    else:
        form = forms.RegisterForm()

    return render(request, "authentication/register.html", {"form": form})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    email = user.email if user.is_authenticated else "user"
    messages.success(request, f"Logged out of {email}")
    logout(request)
    return redirect("home")


@login_required
def edit_view(request: HttpRequest) -> HttpResponse:
    user = request.user

    if request.method == "POST":
        if request.POST.get("action") == "edit":
            edit_form = forms.EditForm(request.POST, instance=user)
            password_form = forms.PasswordForm()

            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, f"User information edited successfully")
                return redirect("home")

        elif request.POST.get("action") == "password":
            edit_form = forms.EditForm(instance=user)
            password_form = forms.PasswordForm(request.POST)

            if password_form.is_valid():
                user.set_password(password_form.cleaned_data["password"])
                user.save()
                login(request, user)
                messages.success(request, f"Password successfully changed")
                return redirect("home")

    else:
        edit_form = forms.EditForm(instance=user)
        password_form = forms.PasswordForm()

    return render(request, "authentication/edit.html", {
            "edit_form": edit_form,
            "password_form": password_form,
        })
