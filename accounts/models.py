from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractUser):
    special_user = models.DateTimeField(default=timezone.now)

    def is_special_user(self):
        if self.special_user > timezone.now:
            return True
        return False
