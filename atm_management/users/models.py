from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    amount = models.IntegerField(default=0)  # Add this field if needed

    def __str__(self):
        return self.username
