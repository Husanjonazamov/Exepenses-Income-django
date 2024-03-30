from django.db import models
from django.contrib.auth.models import User


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self) -> str:
        return self.user

# Create your models here.
