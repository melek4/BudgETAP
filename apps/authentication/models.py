# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.home.models import Department

class User(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    # Add any additional fields or methods as needed

    def __str__(self):
        return self.username

# Create your models here.
