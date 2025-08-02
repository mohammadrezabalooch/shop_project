from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from comments.models import Comment
from django.contrib.contenttypes.fields import GenericRelation


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
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name="articles",
    )
    is_special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="postimages/%Y/%m/%d/", null=True, blank=True)

    comment = GenericRelation(Comment)

    def get_absolute_url(self):
        return reverse("postdetail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title[:20]
