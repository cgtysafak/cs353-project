from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views
from django.urls import path, include


urlpatterns = [
    path('home/', views.HomeView.as_view(),  name="home"),
    path('users/', views.UsersView.as_view(), name="users"),
    path('login/', views.LoginView.as_view(), name="login"),

]
