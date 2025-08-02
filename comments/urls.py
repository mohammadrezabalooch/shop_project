from django.urls import path
from .views import AddComment

urlpatterns = [
    path("add/", AddComment.as_view(), name="commentadd"),
]
