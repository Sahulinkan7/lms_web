from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    