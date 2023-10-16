# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, user_management, modify_user, delete_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", user_management, name="users"),
    path('users/modify_user/<int:user_id>/', modify_user, name='modify_user'),
    path('users/delete_user/<int:user_id>/', delete_user, name='delete_user'),
]
