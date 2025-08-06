from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    image = models.ImageField(
        upload_to="productimages/%Y/%m/%d/", null=True, blank=True
    )

    comments = GenericRelation(Comment)

    def approved_comments(self):
        return self.comments.filter(is_approved=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("productdetail", kwargs={"pk": self.pk})
