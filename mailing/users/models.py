from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role_choices = [
        ('user', 'User'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(
        max_length=10, choices=role_choices, default='user')

    is_active = models.BooleanField(default=True)
    token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.username} - {role}'
