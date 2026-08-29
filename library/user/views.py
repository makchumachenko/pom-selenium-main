from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import permissions, viewsets

from . import serializers

User = get_user_model()


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, "user/user_list.html", {"users": users})


@login_required
def user_info(request, id: int):
    user = User.objects.get(pk=id)
    return render(request, "user/user.html", {"user": user})


class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all().order_by("id")
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by("id")
        user = self.request.user

        if not user.is_staff:
            queryset = queryset.filter(pk=user.id)

        return queryset

    def get_permissions(self):
        return ([permissions.IsAuthenticated()]
            if self.action in ("list", "retrieve")
            else [permissions.IsAdminUser()])
    