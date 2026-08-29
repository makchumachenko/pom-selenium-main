from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "auth"

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.edit_view, name='edit'),
]