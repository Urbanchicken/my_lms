from django.db import models
from django.contrib.auth.models import AbstractUser

role_choices = [
    ('Librarian', 'Librarian'),
    ('Student', 'Student'),
]

class CustomUser(AbstractUser):
    std_number = models.BigIntegerField(unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures")
    role = models.CharField(max_length=63, choices=role_choices)

