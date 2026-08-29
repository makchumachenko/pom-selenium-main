"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from author.views import AuthorViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from user.views import UserViewSet

from . import views

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"author", AuthorViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("book/", include("book.urls")),
    path("order/", include("order.urls")),
    path("auth/", include("authentication.urls")),
    path("author/", include("author.urls")),
    path("user/", include("user.urls")),
    path("", views.home, name="home"),
    path("api/<str:version>/", include(router.urls)),
    path(
        "api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    path("api/<str:version>/book/", include("book.api_urls")),
    path("api/<str:version>/order/", include("order.api_urls")),
    path("api/<str:version>/user/", include("user.api_urls")),
]
