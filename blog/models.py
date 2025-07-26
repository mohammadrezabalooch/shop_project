from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    status_choices = (
        ("p", "publish"),
        ("d", "draft"),
        ("b", "back"),
    )
    status = models.CharField(choices=status_choices, max_length=1)
    author = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        related_name="articles",
    )
    is_special = models.BooleanField(default=False)
